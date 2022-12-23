from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Катагория (Тип)'
        verbose_name_plural = 'Категории (Типы)'


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True
    )
    genre = models.ManyToManyField(Genre, through='GenresTitles')

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']


class GenresTitles(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение:Жанры'
        verbose_name_plural = 'Произведения:Жанры'

    def __str__(self):
        return f'{self.title} {self.genre}'


class ReviewComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.author

    class Meta:
        abstract = True
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ['pub_date', 'review']


class Review(ReviewComment):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, "Значение не больше %(limit_value)."),
            MinValueValidator(1, "Значение не меньше %(limit_value).")])


    class Meta(ReviewComment.Meta):
        verbose_name = 'Отзыв на произведение'
        verbose_name_plural = 'Отзывы на произведение'
        ordering = ['pub_date', 'title']
        constraints = [UniqueConstraint(fields=['author', 'title'],
                                        name='double_review')]
        default_related_name = 'reviews'


class Comment(ReviewComment):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta(ReviewComment.Meta):
        default_related_name = 'comments'
