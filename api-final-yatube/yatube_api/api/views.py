from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, User
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
    UserSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Управление постами: чтение для всех,
    правка только для автора.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Назначить автора при создании поста."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Управление комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )

    def get_post(self):
        """Получить объект поста."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Вернуть все комментарии, относящиеся к выбранному посту."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Назначить автора и связать комментарий с постом."""
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предоставление данных групп только для чтения."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Управление подписками текущего пользователя."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Вернуть список подписок текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Создать новую подписку."""
        serializer.save()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Предоставление данных пользователей только для чтения."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
