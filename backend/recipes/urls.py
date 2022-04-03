from django.urls import include, path
from rest_framework.routers import SimpleRouter
from recipes.views import RecipeViewSet
from recipes.views import IngredientsViewSet, TagsViewSet


app_name = 'recipes'

router = SimpleRouter()
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
