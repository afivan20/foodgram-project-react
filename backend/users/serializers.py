from django.shortcuts import get_object_or_404
from users.models import User, Follow
from recipes.models import Recipe
from rest_framework import serializers
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex="^[\w.@+-]+\Z",
                message=(
                    "Username состоит из "
                    "букв, цифр, символов подчеркивания, точек и дефисов."
                ),
                code="invalid_username",
            ),
        ],
    )
    is_subscribed = serializers.SerializerMethodField(
        read_only=True, method_name="get_is_subscribed"
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_subscribed(self, obj):
        request_user = self.context.get("request").user.id
        return Follow.objects.filter(user=request_user, author=obj).exists()


class FollowingRecipesSerializer(serializers.ModelSerializer):
    """Отдает рецепты в сокращенной форме."""

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки POST, DELETE."""

    is_subscribed = serializers.SerializerMethodField(
        method_name="get_is_subscribed"
    )
    recipes = serializers.SerializerMethodField(
        method_name="get_recipes"
    )
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipes_count"
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        request_user = self.context.get("request").user.id
        return Follow.objects.filter(user_id=request_user, author=obj).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.pk).count()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        author = get_object_or_404(User, id=obj.pk)
        recipes = author.recipes_author.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = FollowingRecipesSerializer(
            recipes,
            many=True,
            context={
                "request": request,
            },
        )
        return serializer.data


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализатор полей подписчиков GET."""

    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField(
        method_name="get_is_subscribed"
    )
    recipes = serializers.SerializerMethodField(method_name="get_recipes")
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipes_count"
    )

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        author = get_object_or_404(User, username=obj.author)
        recipes = author.recipes_author.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = FollowingRecipesSerializer(
            recipes,
            many=True,
            context={
                "request": request,
            },
        )
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user.id
        return Follow.objects.filter(user_id=user, author=obj.author).exists()

    def get_recipes_count(self, obj):
        print(obj.author)
        author = get_object_or_404(User, username=obj.author)
        recipes = author.recipes_author.all().count()
        return recipes
