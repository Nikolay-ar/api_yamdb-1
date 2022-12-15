from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import response, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User
from api.permissions import IsUserOrIsModeratorOrAdminOrReadOnly
from users.serializers import (AdminUserSerializer, AuthentificationSerializer,
                               RegistrationSerializer, UserSerializer)
from django.core.mail import send_mail
from http import HTTPStatus
from api_yamdb.settings import DEFAULT_FROM_EMAIL

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user= User.objects.get_or_create(username=username,
                                         email=email)
    confirmation_code = user._gen_confirm_code()
    message = (f'Код подтверждения: {confirmation_code}')                                         
    send_mail(
            subject='Подтверждение e-mail',
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[],
            fail_silently=False,
        ) 
    return Response({'detail': 'Сообщение успешно отправлено'},
                        status=HTTPStatus.OK.value)
# очень много вопросов как будет работать, надо пробовать по тестам как и отправится ли вообще сообщение

@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation_view(request):
    serializer = AuthentificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, code):
        return response.Response(
            data={'error': 'некорректный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = user.token
    return response.Response(
        data={'access': str(token)},
        status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsUserOrIsModeratorOrAdminOrReadOnly,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
