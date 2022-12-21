from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UsernameValidator

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = (
    (ADMIN, 'Administrator'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
)


class User(AbstractUser):
    """Создание кастомного класса User, описание базовых функций"""

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        validators=[UsernameValidator()],
        verbose_name='Никнейм'
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )

    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография/О пользователе',
        help_text='Расскажите о себе'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя'
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self):
        return self.username
