from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.constants import ADMIN_EMPTY_VALUE_DISPLAY
from users.models import Follow, User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """Управление пользователями."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Персональные данные',
            {
                'fields': ('first_name', 'last_name', 'email'),
            },
        ),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Управление подписками."""

    list_display = ('id', 'user', 'author')
    search_fields = (
        'user__username',
        'user__email',
        'author__username',
        'author__email',
    )
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY
