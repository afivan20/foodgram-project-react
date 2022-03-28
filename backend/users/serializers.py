from django.forms import SlugField
from users.models import User
from rest_framework import serializers
from django.core.validators import RegexValidator

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True,
                                    validators=[RegexValidator(regex='^[\w.@+-]+\Z', message='Username must be буквы, цифры, символы подчеркивания, точки и дефисы.',
                                    code='invalid_username'),]
                                    )



    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password',
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

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name',
        )