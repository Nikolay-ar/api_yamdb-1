from django.contrib import admin

from .models import Categories, Genres, Titles, GenresTitles


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description', 'rating', 'сategory', 'genre')
    list_editable = ('category',)
    search_fields = ('year', 'name', 'genre',)
    list_filter = ('name',)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class GenresTitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre')
    search_fields = ('title', 'genre')
    list_filter = ('title', 'genre')


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(GenresTitles, GenresTitlesAdmin)
