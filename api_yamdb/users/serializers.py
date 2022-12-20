import re

from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя ' + value + '  запрещено.'
            )
        return value

    def validate(self, data):
        if not User.objects.filter(username=data['username'],
                                   email=data['email']).exists():

            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким имененем существует'
                )
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким email существует'
                )
            return data


class AuthentificationSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role']


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для получения кода авторизации на почту."""

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете зарегистрироваться под именем me')
        if pattern.match(value) is None:
            raise serializers.ValidationError(
                'Username должно соответствовать паттерну')
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
