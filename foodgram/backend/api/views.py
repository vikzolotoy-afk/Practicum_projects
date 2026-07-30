from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import VariablePageSizePagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeActionSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)
from api.utils import generate_shopping_list_text
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Follow, User
from users.serializers import SubscriptionSerializer, UserSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с тегами."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления рецептами."""
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags', 'ingredients', 'favorites', 'shopping_cart'
    )
    pagination_class = VariablePageSizePagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Вернуть сериализатор в зависимости от метода запроса."""
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        """Автоматически сохраненить автора при создании."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавить/удалить из избранного."""
        if request.method == 'POST':
            return self._add_to_list(Favorite, request.user, pk)
        return self._delete_from_list(Favorite, request.user, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавить/удалить из списка покупок."""
        if request.method == 'POST':
            return self._add_to_list(ShoppingCart, request.user, pk)
        return self._delete_from_list(ShoppingCart, request.user, pk)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Агрегация ингредиентов и выгрузка TXT-файла."""
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        if not ingredients.exists():
            return Response({'errors': 'Ваш список покупок пуст'},
                            status=status.HTTP_400_BAD_REQUEST)

        content = generate_shopping_list_text(ingredients)

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment;'
            'filename=shopping_list.txt'
        )
        return response

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        """Создать короткую ссылку на рецепт."""
        recipe = self.get_object()
        return Response(
            {'short-link': request.build_absolute_uri(f'/s/{recipe.id}/')}
        )

    def _add_to_list(self, model, user, pk):
        """Добавить рецепт в список."""
        recipe = get_object_or_404(Recipe, id=pk)

        serializer = RecipeActionSerializer(
            data={'user': user.id, 'recipe': recipe.id},
            model=model,
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_from_list(self, model, user, pk):
        """Удалить рецепт из списка."""
        recipe = get_object_or_404(Recipe, id=pk)

        obj = model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'errors': 'Рецепта нет в вашем списке'},
                        status=status.HTTP_400_BAD_REQUEST)


class MyUserViewSet(UserViewSet):
    """Вьюсет для пользователей с поддержкой подписок и аватаров."""

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Список подписок текущего пользователя."""
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Вернуть список разрешений в зависимости от выполняемого действия."""
        if self.action == "me":
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(
        methods=['get', 'put', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        """Профиль текущего пользователя."""
        return super().me(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        """Подписаться или отписаться от автора."""
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Нельзя на себя подписаться'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=user, author=author)
            return Response(
                SubscriptionSerializer(
                    author, context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED,
            )

        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы не были подписаны'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['put', 'delete'],
        url_path='me/avatar',
        permission_classes=[IsAuthenticated],
    )
    def avatar(self, request):
        """Добавить или удалить аватар текущего пользователя."""
        user = request.user

        if request.method == 'PUT':
            if 'avatar' not in request.data:
                return Response(
                    {'errors': 'Поле avatar является обязательным.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if user.avatar:
                return Response(
                    {'avatar': user.avatar.url},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'errors': 'Не удалось сохранить аватар.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.avatar:
            user.avatar.delete()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


def redirect_short_url(request, id):
    """Обработать переход по короткой ссылке."""
    recipe = get_object_or_404(Recipe, id=id)
    return redirect(f'/recipes/{recipe.id}/')
