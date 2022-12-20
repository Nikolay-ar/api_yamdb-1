from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Катагория (Тип)'
        verbose_name_plural = 'Категории (Типы)'


class Genres(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField()
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='title',
        null=True
    )
    genre = models.ManyToManyField(Genres, through='GenresTitles')

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']


class GenresTitles(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение:Жанры'
        verbose_name_plural = 'Произведения:Жанры'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Reviews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.SmallIntegerField(default=1,
                                     validators=[
                                         MaxValueValidator(10),
                                         MinValueValidator(1)
                                     ])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв на произведение'
        verbose_name_plural = 'Отзывы на произведение'
        ordering = ['pub_date', 'title']


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ['pub_date', 'review']
