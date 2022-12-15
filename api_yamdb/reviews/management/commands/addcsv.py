import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Categories, Genres, Titles,
                            GenresTitles, Review, Comment)
from users.models import User


class Command(BaseCommand):
    file_table = {
        'category.csv': Categories,
        'genre': Genres,
        'titles': Titles,
        'genre_title': GenresTitles,
        'review': Review,
        'comments': Comment,
        'users.csv': User,
    }

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=int)

    def handle(self, *args, **options):
        with open('file_name') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # data = model_table(currency=row['Currency'], name=row['Country'])
                # data.save()

        print('Data Uploaded!!')


