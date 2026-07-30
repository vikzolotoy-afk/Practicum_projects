from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from rest_framework import serializers

from api.fields import Base64ImageField
from recipes.models import Recipe

User = get_user_model()


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    first_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150
    )
    last_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(djoser_serializers.UserSerializer):
    """Сериализатор для работы с профилем пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )

    def get_is_subscribed(self, obj):
        """Проверить, подписан ли текущий пользователь на данного автора."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.following.filter(user=request.user).exists()


class RecipeShortSerializer(serializers.ModelSerializer):
    """Укороченный сериализатор рецептов для списков в подписках/корзине."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для вывода подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes(self, obj):
        """Получить список рецептов автора с учетом параметра лимита."""
        request = self.context.get('request')
        limit = None

        if request:
            limit = request.query_params.get('recipes_limit')

        recipes = obj.recipes.all()

        if limit:
            try:
                recipes = recipes[: int(limit)]
            except (ValueError, TypeError):
                pass
        return RecipeShortSerializer(
            recipes, many=True, context={'request': request}
        ).data
