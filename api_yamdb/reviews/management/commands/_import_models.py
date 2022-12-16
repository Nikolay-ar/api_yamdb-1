import csv

from django.core.management import CommandError
from reviews.models import (Categories, Genres, Titles,
                            GenresTitles, Review, Comment)
from users.models import User


def import_categories():
    with open('data/category.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Categories(id=row['id'],
                                  name=row['name'],
                                  slug=row['slug'])
            data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте category.csv произошла ошибка{error}')


def import_genres():
    with open('data/genre.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Genres(id=row['id'],
                              name=row['name'],
                              slug=row['slug'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте genre.csv произошла ошибка{error}')


def import_titles():
    with open('data/titles.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Titles(id=row['id'],
                              name=row['name'],
                              year=row['year'],
                              description=row['description'],
                              category=Categories.objects.get(
                                  id=row['category'])
                              )
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте titles.csv произошла ошибка{error}')


def import_genres_title():
    with open('data/genre_title.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = GenresTitles(id=row['id'],
                                    title=Titles.objects.get(
                                        id=row['title_id']),
                                    genre=Genres.objects.get(
                                        id=row['genre_id']))
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте genre_title.csv произошла ошибка{error}')


def import_users():
    with open('data/users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = User(id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте users.csv произошла ошибка{error}')


def import_review():
    with open('data/review.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Review(id=row['id'],
                              titles=Titles.objects.get(
                                  id=row['title_id']),
                              text=row['text'],
                              author=User.objects.get(
                                  id=row['author']),
                              score=row['score'],
                              pub_date=row['pub_date'])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте review.csv произошла ошибка{error}')


def import_comments():
    with open('data/comments.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Comment(id=row['id'],
                               review=Review.objects.get(
                                   id=row['review_id'],
                                   text=row['text'],
                                   author=User.objects.get(
                                       id=row['author']),
                                   pub_date=row['pub_date'])
                               )
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте comments.csv произошла ошибка{error}')
