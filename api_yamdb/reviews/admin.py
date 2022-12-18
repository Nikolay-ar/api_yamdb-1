from django.contrib import admin

from .models import Categories, Genres, Titles, GenresTitles, Reviews, Comments


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description', 'category')
    list_editable = ('category',)
    search_fields = ('year', 'name',)
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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('score',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(GenresTitles, GenresTitlesAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Comments, CommentAdmin)
