from django.db.models import Case, IntegerField, When
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = ("author", "tags", "is_favorited", "is_in_shopping_cart")

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    name = filters.CharFilter(method="filter_name")

    class Meta:
        model = Ingredient
        fields = ("name",)

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value).order_by(
            Case(
                When(name__istartswith=value, then=0),
                When(name__icontains=value, then=1),
                default=2,
                output_field=IntegerField(),
            ),
            "name",
        )
