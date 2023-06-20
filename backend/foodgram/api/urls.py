
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserSubscribeView,
    UserSubscriptionsViewSet,
)

v1_router = DefaultRouter()

v1_router.register("tags", TagViewSet, basename="tags")
v1_router.register("ingredients", IngredientViewSet, basename="ingredients")
v1_router.register("recipes", RecipeViewSet, basename="recipes")


urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path(
        "users/subscriptions/",
        UserSubscriptionsViewSet.as_view({"get": "list"}),
    ),
    path("users/<int:user_id>/subscribe/", UserSubscribeView.as_view()),
    path("", include(v1_router.urls)),
    path("", include("djoser.urls")),
]
