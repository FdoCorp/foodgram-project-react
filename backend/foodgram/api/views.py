from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    ShoppingCartSerializer,
    TagSerialiser,
    UserSubscribeRepresentSerializer,
    UserSubscribeSerializer,
)
from api.utils import add_recipe_to_m2m, del_recipe_from_m2m, get_shoping_list
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscription

User = get_user_model()


class UserSubscribeView(APIView):
    """Создание/удаление подписки на пользователя."""

    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscribeSerializer(
            data={"user": request.user.id, "author": author.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(
            user=request.user, author=author
        ).exists():
            return Response(
                {"errors": "Вы не подписаны на этого пользователя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Subscription.objects.get(user=request.user.id, author=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Получение списка всех подписок на пользователей."""

    serializer_class = UserSubscribeRepresentSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации о тегах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами. Создание/изменение/удаление рецепта.
    Получение информации о рецептах.
    Добавление рецептов в избранное и список покупок.
    Отправка файла со списком рецептов.
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeGetSerializer
        if self.action == "favorite":
            return FavoriteSerializer
        if self.action == "shopping_cart":
            return ShoppingCartSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        """Работа с избранными рецептами.
        Удаление/добавление в избранное.
        """
        if request.method == "POST":
            serializer_class = self.get_serializer_class()
            data = add_recipe_to_m2m(pk, request, serializer_class)
            status_code = status.HTTP_201_CREATED
        elif request.method == "DELETE":
            data = del_recipe_from_m2m(pk, request, Favorite)
            status_code = status.HTTP_204_NO_CONTENT
        else:
            data = {"error": "Недопустимый метод."}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status_code)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, pk):
        """Работа со списком покупок.
        Удаление/добавление в список покупок.
        """
        if request.method == "POST":
            serializer_class = self.get_serializer_class()
            data = add_recipe_to_m2m(pk, request, serializer_class)
            status_code = status.HTTP_201_CREATED
        elif request.method == "DELETE":
            data = del_recipe_from_m2m(pk, request, ShoppingCart)
            status_code = status.HTTP_204_NO_CONTENT
        else:
            data = {"error": "Недопустимый метод."}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status_code)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        shopping_list = get_shoping_list(request.user)
        response = HttpResponse(shopping_list, content_type="text/plain")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="shopping_cart.txt"'
        return response
