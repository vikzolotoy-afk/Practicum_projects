from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from recipes import constants
from recipes.validators import validate_slug

User = get_user_model()


class BaseModel(models.Model):
    """Базовая абстрактная модель: добавляет поле name и метод __str__."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_NAME_LENGTH
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class UserRecipeBaseModel(models.Model):
    """Абстрактная модель для связи Пользователь + Рецепт."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class Tag(BaseModel):
    """Модель для тегов рецептов."""

    slug = models.SlugField(
        'Уникальный слаг',
        max_length=constants.MAX_TAG_LENGTH,
        unique=True,
        validators=[validate_slug],
        help_text='Уникальный слаг тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Ingredient(BaseModel):
    """Модель для ингредиентов."""

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=constants.MAX_UNIT_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(BaseModel):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/'
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список тегов'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                constants.MIN_COOKING_TIME,
                message=f'Минимум — {constants.MIN_COOKING_TIME} мин.'
            )
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def get_short_link(self):
        """Вернуть относительную короткую ссылку на рецепт."""
        return f'/s/{self.id}/'


class IngredientInRecipe(models.Model):
    """Связующая модель ингредиентов и рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_list',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                constants.MIN_INGREDIENT_AMOUNT,
                message=f'Минимум — {constants.MIN_INGREDIENT_AMOUNT}'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} — {self.amount}'


class Favorite(UserRecipeBaseModel):
    """Модель для добавления рецептов в избранное."""

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]


class ShoppingCart(UserRecipeBaseModel):
    """Модель для списка покупок."""

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_cart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart'
            )
        ]
