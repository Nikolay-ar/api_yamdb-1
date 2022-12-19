from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (UserSerializer, SignUpSerializer, GetTokenSerializer)
from api.permissions import IsAdmin
from api_yamdb.settings import DEFAULT_FROM_EMAIL


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """Функция для получения кода авторизации на почту."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    # confirmation_code = get_random_string(12)
    new_user = User.objects.create_user(
        username=username,
        email=email,
    )
    new_user.save()
    confirmation_code = default_token_generator.make_token(new_user)
    send_mail(
        subject='Код подтверждения',
        message=f'Регистрация прошла успешно! '
                f'Код подтверждения: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation_view(request):
    """Функция для получения токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = request.data.get('confirmation_code')
    # confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, code):
        response = {'Неверный код'}
        return Response(response, status=HTTP_400_BAD_REQUEST)
    token = str(RefreshToken.for_user(user).access_token)
    response = {'token': token}
    return Response(response, status=HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    search_fields = ('username',)

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        """Редактирование и получение информации профиля."""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=HTTPStatus.OK.value
            )
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(
                serializer.data,
                status=HTTPStatus.OK.value
            )
