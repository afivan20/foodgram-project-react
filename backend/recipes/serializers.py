from rest_framework import serializers
from users.models import Follow
from users.models import User
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientAmount,
    ShoppingCart
)
from drf_base64.fields import Base64ImageField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from django.db import transaction


class AuthorSerializer(serializers.ModelSerializer):
    """Сериалазейзер для отображения поля author в рецепте."""

    is_subscribed = serializers.SerializerMethodField(
        method_name="get_is_subscribed"
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj.pk).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериалазейзер для отображения поля tags в рецепте."""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалазейзер для отображения поля ingredients в рецепте."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")
        read_only_fields = ("id", "name", "measurement_unit")


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Сериалазейзер для отображения дополнительного поля amount рецепта
    в .to_representation().
    """

    id = serializers.PrimaryKeyRelatedField(
        source="ingredient", queryset=Ingredient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )
    name = serializers.CharField(source="ingredient.name", read_only=True)

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=(
                    "ingredient",
                    "recipe",
                ),
            )
        ]


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериалазейзер для отображения рецепта в .to_representation()"""

    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountSerializer(source="amounts", many=True)
    is_favorited = serializers.SerializerMethodField(
        method_name="get_is_favorited"
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name="get_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user.pk,
            recipe=obj.pk
        ).exists()


class IngredientAmountCreateSerializer(serializers.ModelSerializer):
    """Сериалазейзер для создания рецепта с дополнительным полем amount."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmount
        fields = ("id", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалазейзер для рецептов GET, POST, PATCH, DELETE."""

    author = AuthorSerializer(
        read_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    image = Base64ImageField()
    ingredients = IngredientAmountCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def to_representation(self, instance):
        request = self.context.get("request")
        serializer = RecipeListSerializer(
            instance,
            context={
                "request": request,
            },
        )
        return serializer.data

    def create(self, validated_data):
        author = validated_data.get("author")
        name = validated_data.get("name")
        text = validated_data.get("text")
        cooking_time = validated_data.get("cooking_time")
        image = validated_data.pop("image")
        tags_data = validated_data.pop("tags")
        try:
            with transaction.atomic():
                recipe = Recipe.objects.create(
                    author=author,
                    name=name,
                    text=text,
                    image=image,
                    cooking_time=cooking_time,
                )
                for tag in tags_data:
                    recipe.tags.add(tag)
                ingredients_data = validated_data.pop("ingredients")
                for count_ingredient in ingredients_data:
                    IngredientAmount.objects.create(
                        ingredient=count_ingredient["id"],
                        recipe=recipe,
                        amount=count_ingredient["amount"],
                    )
        except Exception:
            raise serializers.ValidationError("Ошибка при создании рецепта")
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        try:
            with transaction.atomic():
                instance.tags.clear()
                tags_data = self.initial_data.get("tags")
                instance.tags.set(tags_data)
                IngredientAmount.objects.filter(recipe=instance).all().delete()
                ingredients = validated_data.get("ingredients")
                for ingredient in ingredients:
                    IngredientAmount.objects.create(
                        ingredient=ingredient["id"],
                        recipe=instance,
                        amount=ingredient["amount"],
                    )
                instance.save()
        except Exception:
            raise serializers.ValidationError("Ошибка при создании рецепта")
        return instance

    def validate(self, data):
        ingredients_data = self.initial_data.get("ingredients")
        ingredients_added = []
        for ingredient in ingredients_data:
            ingredient_name = get_object_or_404(
                Ingredient, id=ingredient["id"]
            )
            if ingredient_name in ingredients_added:
                raise serializers.ValidationError("Не дублируйте ингредиенты")
            ingredients_added.append(ingredient_name)
        return data
