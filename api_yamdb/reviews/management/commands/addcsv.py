from _import_models import *

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            import_categories()
            import_genres()
            import_titles()
            import_genres_title()
            import_users()
            import_review()
            import_comments()
        except Exception as error:
            raise CommandError(f'Сбой при импорте: {error}')

        self.stdout.write(self.style.SUCCESS('Импорт прошел успешно'))
