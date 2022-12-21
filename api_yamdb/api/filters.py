import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    class Meta:
        model = Title
        fields = ['name', 'year']
