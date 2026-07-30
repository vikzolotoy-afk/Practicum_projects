from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне объекта: редактирование разрешено только автору.
    Для всех остальных пользователей разрешено только чтение.
    """

    def has_object_permission(self, request, view, obj):
        """Проверить право автора на правку текущего объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
