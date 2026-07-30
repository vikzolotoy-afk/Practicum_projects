from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    signup,
    get_token,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet
)


router_v1_api = DefaultRouter()
router_v1_api.register(r'users', UserViewSet, basename='users')
router_v1_api.register(r'titles', TitleViewSet, basename='titles')
router_v1_api.register(r'genres', GenreViewSet, basename='genres')
router_v1_api.register(r'categories', CategoryViewSet, basename='categories')
router_v1_api.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router_v1_api.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1_api.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
]
