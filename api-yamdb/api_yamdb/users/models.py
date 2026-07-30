from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.constants import EMAIL_FIELD_LENGTH, USERNAME_FIELD_LENGTH
from users.validators import username_not_me


username_validation = UnicodeUsernameValidator()


class UserRole(models.TextChoices):
    USER = "user", "User"
    MODERATOR = "moderator", "Moderator"
    ADMIN = "admin", "Admin"


class User(AbstractUser):
    """
    Переопределенная модель User.
    Содержит бизнес-роли класса UserRole.
    Переопределяет поле email, оно обязательно для отправки кода.
    """
    username = models.CharField(
        max_length=USERNAME_FIELD_LENGTH,
        unique=True,
        validators=[username_validation, username_not_me],
        error_messages={
            "unique": ("Юзер с таким именем уже существует."),
        },
        verbose_name='Никнейм пользователя'
    )
    email = models.EmailField(
        unique=True,
        max_length=EMAIL_FIELD_LENGTH,
        verbose_name='Почтовый адрес',
        error_messages={
            "unique": ("Юзер с таким email уже существует."),
        },
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=max([len(c.value) for c in UserRole]),
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self) -> bool:
        return (
            self.role == UserRole.ADMIN or self.is_superuser or self.is_staff
        )

    @property
    def is_moderator(self) -> bool:
        return self.role == UserRole.MODERATOR
