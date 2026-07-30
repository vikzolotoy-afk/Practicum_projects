from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка админ-панели для отзывов."""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('text', 'author__username', 'title__name')
    list_filter = ('pub_date', 'score')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка админ-панели для комментариев."""

    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('text', 'author__username')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админ-панели для категорий."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка админ-панели для жанров."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка админ-панели для произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'get_genres',
    )
    search_fields = ('name', 'description')
    list_filter = ('year', 'category')
    filter_horizontal = ('genre',)
    empty_value_display = '-пусто-'

    @admin.display(description='Жанры')
    def get_genres(self, obj):
        """Выводит все жанры произведения через запятую."""
        return ', '.join(genre.name for genre in obj.genre.all())

    get_genres.short_description = 'Жанры'
