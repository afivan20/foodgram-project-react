from rest_framework import viewsets
from recipes.models import Ingredient, Tag, Recipe, Favorite, ShoppingCart
from recipes.serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from users.serializers import FollowingRecipesSerializer
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

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

    @action(methods=['post', 'delete'], permission_classes=[IsAuthenticated], detail=True)
    def favorite(self, request, pk):
        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response({'errors': 'Вы уже добавили рецепт.'}, status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = FollowingRecipesSerializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = Favorite.objects.filter(user=request.user, recipe__id=pk)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Этот рецепт уже не в избранных :( '}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], permission_classes=[IsAuthenticated], detail=True)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response({'errors': 'Вы уже добавили рецепт.'}, status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = FollowingRecipesSerializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = ShoppingCart.objects.filter(user=request.user, recipe__id=pk)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Этот рецепт уже удален :( '}, status=status.HTTP_400_BAD_REQUEST)


