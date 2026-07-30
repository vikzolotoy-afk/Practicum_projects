from rest_framework import serializers

from api.validators import validate_not_empty
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Преобразование данных отзывов в JSON."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(validators=[validate_not_empty])

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверить: один пользователь — один отзыв на произведение."""
        request = self.context.get('request')
        if request and request.method == 'POST':
            author = request.user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                author=author,
                title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    {'title': 'Вы уже оставили отзыв на это произведение.'}
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Преобразование данных комментариев в JSON."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(validators=[validate_not_empty])

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
