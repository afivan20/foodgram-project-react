from users.models import User, Follow
from recipes.models import Recipe
from rest_framework import serializers
from django.core.validators import RegexValidator
from drf_base64.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[RegexValidator(regex='^[\w.@+-]+\Z', message='Username must be буквы, цифры, символы подчеркивания, точки и дефисы.',
                                                                code='invalid_username'), ]
                                     )
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed',
        )
        extra_kwargs = {
            'password': {'write_only': True, },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        return Follow.objects.filter(
            user=request_user, author=obj
        ).exists()


class UserDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', )

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        return Follow.objects.filter(
            user=request_user, author=obj
        ).exists()


class FollowingRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        #read_only_fields = ('id', 'name', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',   'recipes',
                  'recipes_count'
                  )

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        return Follow.objects.filter(
            user_id=request_user, author=obj
        ).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.pk).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.pk)
        if limit:
            queryset = queryset[:int(limit)]
        serializer = FollowingRecipesSerializer(queryset, many=True, context={'request': request, })
        return serializer.data


class SubscriptionsSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ( 'email', 'id','username', 'first_name', 'last_name', 'is_subscribed',
                    'recipes', 'recipes_count',)
    
    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        serializer = FollowingRecipesSerializer(queryset, many=True, context={'request': request, })
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user.id
        return Follow.objects.filter(
            user_id=user, author=obj.author
        ).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
