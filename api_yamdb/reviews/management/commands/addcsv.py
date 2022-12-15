from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Categories, Genres, Titles,
                            GenresTitles, Review, Comment)
from users.models import User


class Command(BaseCommand):
    file_table = {

    }

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))


def import_countries(request):
    with open(
            'C:/python/Azuro/azuro_django/pms/templates/pms/countryname.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = Country(currency=row['Currency'], name=row['Country'])
            data.save()

    return HttpResponse('Data Uploaded!!')