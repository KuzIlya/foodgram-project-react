from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .constants import EMPTY_VALUE_TEXT
from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = ('password',)
    list_filter = ('email', 'first_name',)
    search_fields = ('username', 'email',)
    empty_value_display = EMPTY_VALUE_TEXT


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_editable = ('user', 'author',)
    empty_value_display = EMPTY_VALUE_TEXT
