from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

MAX_LENGTH = 200


class Group(models.Model):
    """Модель для тематических групп публикаций."""

    title: models.CharField = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название группы'
    )
    slug: models.SlugField = models.SlugField(
        unique=True,
        verbose_name='Адрес'
    )
    description: models.TextField = models.TextField(
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для хранения публикаций пользователей."""

    text: models.TextField = models.TextField(
        verbose_name='Текст поста'
    )
    pub_date: models.DateTimeField = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image: models.ImageField = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/',
        null=True,
        blank=True
    )
    group: models.ForeignKey = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев к публикациям."""

    author: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    post: models.ForeignKey = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    text: models.TextField = models.TextField(
        verbose_name='Текст комментария'
    )
    created: models.DateTimeField = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    """Модель для системы подписок пользователей."""

    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
