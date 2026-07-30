from api.views.auth_views import signup, get_token
from api.views.feedback_views import ReviewViewSet, CommentViewSet
from api.views.tgc_views import GenreViewSet, CategoryViewSet, TitleViewSet
from api.views.user_views import UserViewSet

__all__ = [
    'signup',
    'get_token',
    'ReviewViewSet',
    'CommentViewSet',
    'GenreViewSet',
    'CategoryViewSet',
    'TitleViewSet',
    'UserViewSet'
]
