from rest_framework import serializers

from .models import User
from users.validators import username_validator
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=settings.FIELD_EMAIL_LENGTH)
    username = serializers.CharField(max_length=settings.FIELD_MAX_LENGTH,
                                     validators=[username_validator])

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете зарегистрироваться под именем me')
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=settings.FIELD_TOKEN_LENGTH,
        validators=[username_validator]
    )
    confirmation_code = serializers.CharField(
        max_length=settings.FIELD_TOKEN_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
