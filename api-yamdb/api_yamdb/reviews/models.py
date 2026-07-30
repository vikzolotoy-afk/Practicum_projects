from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from reviews.constants import MAX_SCORE, MIN_SCORE, MAX_LENGTH
from reviews.validators import validate_year


User = get_user_model()


class NameSlugBaseModel(models.Model):
    """Абстрактная модель с name и slug."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        """Строковое представление объекта."""
        return self.name[:30]


class Genre(NameSlugBaseModel):
    """Модель жанра. Наследуется от NameSlugBaseModel."""

    class Meta(NameSlugBaseModel.Meta):
        """
        Метаданные.

        verbose_name(plural): имя модели в единственном (множественном) числе.
        """

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(NameSlugBaseModel):
    """Модель категории."""

    class Meta(NameSlugBaseModel.Meta):
        """
        Метаданные.

        ordering: сортировка по названию.
        verbose_name(plural): имя модели в единственном (множественном) числе.
        """

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры'
    )

    class Meta:
        """
        Метаданные.

        ordering: сортировка по названию.
        verbose_name(plural): имя модели в единственном (множественном) числе.
        """

        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Строковое представление объекта."""
        return f"Произведение: {self.name[:30]}"


class Review(models.Model):
    """Модель для отзывов к произведениям."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'


class Comment(models.Model):
    """Модель для комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review.id}'
