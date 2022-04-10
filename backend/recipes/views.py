from rest_framework import viewsets
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
    IngredientAmount,
)
from recipes.serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer
)
from recipes.permissions import IsAuthenticatedAndOwner
from users.serializers import FollowingRecipesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from foodgram import settings
from recipes.filters import RecipeFilter, IngredientFilter
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)

    def get(self, request):
        serializer = self.serializer_class(
            self.get_queryset(),
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedAndOwner]
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def favorite(self, request, pk):
        if request.method == "POST":
            if Favorite.objects.filter(
                user=request.user,
                recipe__id=pk
            ).exists():
                return Response(
                    {"errors": "Вы уже добавили рецепт."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = FollowingRecipesSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            recipe = Favorite.objects.filter(user=request.user, recipe__id=pk)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"errors": "Этот рецепт уже не в избранных :( "},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            if ShoppingCart.objects.filter(
                user=request.user,
                recipe__id=pk
            ).exists():
                return Response(
                    {"errors": "Вы уже добавили рецепт."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = FollowingRecipesSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            recipe = ShoppingCart.objects.filter(
                user=request.user,
                recipe__id=pk
            )
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"errors": "Этот рецепт уже удален :( "},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def pdf_canvas(dict):
        x, y = 45, 710
        response = HttpResponse(content_type=settings.CONTENT_TYPE)
        canvas = Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(TTFont(settings.FONT, settings.FONT_DIR))
        canvas.setFont(settings.FONT, settings.TITLE_SIZE)
        canvas.setTitle(settings.PDF_TITLE)
        canvas.drawString(x, y + 35, settings.TITLE)
        canvas.setFont(settings.FONT, settings.TEXT_SIZE)
        for number, item in enumerate(dict, start=1):
            if y < 120:
                y = 710
                canvas.showPage()
            canvas.drawString(
                x,
                y,
                f'{number}. {item["ingredient__name"]} - '
                f'{item["sum_amount"]}'
                f' {item["ingredient__measurement_unit"]};',
            )
            y -= 35
        canvas.showPage()
        canvas.save()
        return response

    @action(
        methods=["get"],
        permission_classes=[IsAuthenticated],
        detail=False
    )
    def download_shopping_cart(self, request):
        ingredients_list = (
            IngredientAmount.objects.filter(
                recipe__shoppingcart__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(sum_amount=Sum("amount"))
        )
        return self.pdf_canvas(ingredients_list)
