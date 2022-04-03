from rest_framework import viewsets
from recipes.models import Ingredient, Tag, Recipe
from recipes.serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_class = AuthorAndTagFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
