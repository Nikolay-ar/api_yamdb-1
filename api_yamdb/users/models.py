from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    """Выбор роли пользователя"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    """Создание кастомного класса User, описание базовых функций"""

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name='Никнейм'
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Введите имя'
    )

    second_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Фамилия',
        help_text='Введите фамилию, если ее нет оставьте пустую строку'
    )

    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография/О пользователе',
        help_text='Расскажите о себе'
    )
    role = models.CharField(
        choices=Roles,
        default=Roles.USER,
        blank=True,
        verbose_name='Выбор роли пользователя'
    )

    @property
    def is_user(self):
        return self.role == Roles.USER

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN

    def __str__(self):
        return self.username
