from django.db.models import Sum
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, RecipeIngredient
from rest_framework import status


def create_ingredients(ingredients, recipe):
    """Вспомогательная функция для добавления ингредиентов.
    Используется при создании/редактировании рецепта."""
    recipe_ingredients = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(
            Ingredient, id=ingredient.get("id")
        )
        amount = ingredient.get("amount")
        recipe_ingredients.append(
            RecipeIngredient(
                recipe=recipe, ingredient=current_ingredient, amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(recipe_ingredients)


def add_del_recipe_to_m2m(recipe_pk, request, serializer_class, model):
    """Добавить или удалить рецепт в попупки/избранное."""
    if request.method == "POST":
        data = {"user": request.user.pk, "recipe": recipe_pk}
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data, status.HTTP_201_CREATED

    if request.method == "DELETE":
        deleted, _ = (
            model.objects.filter(user=request.user, recipe=recipe_pk)
            .first()
            .delete()
        )
        if deleted:
            return None, status.HTTP_204_NO_CONTENT
        return (
            {"errors": "У вас нет этого рецепта в избранном"},
            status.HTTP_400_BAD_REQUEST,
        )

def get_shoping_list(user):
    ingredients = (
        RecipeIngredient.objects.filter(recipe__carts__user=user)
        .values("ingredient__name", "ingredient__measurement_unit")
        .annotate(ingredient_amount=Sum("amount"))
    )
    shopping_list = ["Список покупок:\n"]
    for ingredient in ingredients:
        name = ingredient["ingredient__name"]
        unit = ingredient["ingredient__measurement_unit"]
        amount = ingredient["ingredient_amount"]
        shopping_list.append(f"\n{name} - {amount}, {unit}")

    return shopping_list
