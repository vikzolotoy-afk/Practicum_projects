from django.contrib.auth.models import AbstractUser
from django.db import models

from users import constants
from users.validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True
    )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=constants.MAX_USER_FIELDS_LENGTH,
        unique=True,
        validators=[validate_username],
    )
    first_name = models.CharField(
        'Имя',
        max_length=constants.MAX_USER_FIELDS_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=constants.MAX_USER_FIELDS_LENGTH
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/avatars/',
        null=True,
        default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class UserRelationshipMixin(models.Model):
    """Абстрактная модель для связи сущности с пользователем."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Кто подписывается'
    )

    class Meta:
        abstract = True


class Follow(UserRelationshipMixin):
    """Модель подписки на авторов рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        default_related_name = 'follower'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
