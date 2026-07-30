from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.fields import Base64ImageField
from api.validators import validate_ingredients_data, validate_tags_data
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.serializers import RecipeShortSerializer, UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:

        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:

        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в составе рецепта."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:

        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для безопасных методов чтения рецептов (GET)."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredient_list'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:

        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Проверить добавление рецепта в избранное текущим пользователем."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверить добавление рецепта в корзину текущим пользователем."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=request.user).exists()


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для записи ингредиентов."""

    id = serializers.IntegerField()

    class Meta:

        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для методов записи рецептов (POST, PATCH, PUT)."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:

        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        """Проверить данные через валидаторы."""
        ingredients = self.initial_data.get("ingredients")
        tags = self.initial_data.get('tags')
        validate_ingredients_data(ingredients)
        validate_tags_data(tags)

        return data

    def create_ingredients(self, ingredients, recipe):
        """Сохранить ингредиенты в связующую таблицу."""
        for item in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=item['id'],
                amount=item['amount'],
            )

    def create(self, validated_data):
        """Создать новый рецепт."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Обновить существующий рецепт."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredient_list.all().delete()
        self.create_ingredients(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Определить формат ответа после записи данных."""
        return RecipeReadSerializer(instance, context=self.context).data


class RecipeActionSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в списки."""

    class Meta:
        model = None
        fields = ('user', 'recipe')

    def __init__(self, *args, **kwargs):
        """Динамически настраивать модель и валидаторы при инициализации."""
        model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        if model:
            self.Meta.model = model
            self.validators = [
                UniqueTogetherValidator(
                    queryset=model.objects.all(),
                    fields=('user', 'recipe'),
                    message='Рецепт уже добавлен в этот список.'
                )
            ]

    def to_representation(self, instance):
        """Вернуть информацию о рецепте в ответе."""
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data
