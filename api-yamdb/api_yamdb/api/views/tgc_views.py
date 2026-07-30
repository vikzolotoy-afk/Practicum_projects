from rest_framework import filters, mixins, viewsets
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateUpdateSerializer
)
from reviews.models import Category, Genre, Title


class NameSlugViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)

    http_method_names = ['get', 'post', 'delete']

    lookup_field = 'slug'

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(NameSlugViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(NameSlugViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).select_related(
        'category'
    ).prefetch_related(
        'genre',
        'reviews'
    ).order_by('name')

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TitleFilter

    http_method_names = ['get', 'post', 'patch', 'delete']

    search_fields = ['name']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer
