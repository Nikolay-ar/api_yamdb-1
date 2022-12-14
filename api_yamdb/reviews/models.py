from django.db import models


class Categories(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Катагория (Тип)'
        verbose_name_plural = 'Категории (Типы)'


class Genres(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField('Год выпуска')
    description = models.TextField()
    rating = models.IntegerField('Рейтинг', default=None)
    сategory = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='title',
    )
    genre = models.ForeignKey(
        Genres, on_delete=models.SET_NULL,
        related_name='title',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenresTitles(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
