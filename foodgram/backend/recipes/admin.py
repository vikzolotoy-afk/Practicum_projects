from django.contrib import admin

from recipes import constants
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


class IngredientInRecipeInline(admin.TabularInline):
    """Настройка отображения ингредиентов внутри формы рецепта."""

    model = IngredientInRecipe
    extra = constants.ADMIN_INLINE_EXTRA
    min_num = constants.ADMIN_INLINE_MIN_NUM


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Интерфейс администрирования для управления рецептами."""

    list_display = ('id', 'name', 'author', 'get_favorites_count')
    list_filter = ('tags',)
    search_fields = ('name', 'author__username', 'author__email')
    inlines = (IngredientInRecipeInline,)

    @admin.display(description='Добавлений в избранное')
    def get_favorites_count(self, obj):
        """Вернуть общее количество добавлений данного рецепта в избранное."""
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Интерфейс администрирования для управления ингредиентами."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Интерфейс администрирования для управления тегами."""

    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(IngredientInRecipe)
