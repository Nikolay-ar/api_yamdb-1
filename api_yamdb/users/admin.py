from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'second_name', 'role')
    search_fields = ('username',)
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
