from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.permissions import IsAuthorOrStaffOrReadOnly
from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Управление отзывами к произведениям."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        """Получить объект произведения."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Вернуть список отзывов для конкретного произведения."""
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Назначить автора и произведение при создании отзыва."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Управление комментариями к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Получить объект отзыва."""
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Вернуть список комментариев для конкретного отзыва."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Назначить автора и отзыв при создании комментария."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
