from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


def validate_not_empty(value):
    """Валидатор для проверки на пустоту и пробелы."""
    if not value or not value.strip():
        raise serializers.ValidationError('Поле не может быть пустым.')
    return value


class UserSerializer(serializers.ModelSerializer):
    """Преобразование данных пользователя в JSON."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')


class PostSerializer(serializers.ModelSerializer):
    """Преобразование данных постов в JSON."""

    author: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(validators=[validate_not_empty])
    group: serializers.PrimaryKeyRelatedField = (
        serializers.PrimaryKeyRelatedField(
            queryset=Group.objects.all(),
            required=False,
            allow_null=True
        )
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class CommentSerializer(serializers.ModelSerializer):
    """Преобразование данных комментариев в JSON."""

    author: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Преобразование данных групп в JSON."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Преобразование данных подписок в JSON."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого автора'
            )
        ]

    def validate(self, data):
        """Проверить подписки на самого себя."""
        if self.context['request'].user == data.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data
