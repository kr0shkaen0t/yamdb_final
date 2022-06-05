from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import User
from reviews.validators import year_validator


class Category(models.Model):
    """Ресурс Category"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Человекочитаемый идентификатор страницы',
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return '{}: {}'.format(self.name, self.slug)


class Genre(models.Model):
    """Ресурс Genre."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Человекочитаемый идентификатор страницы',
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return '{}: {}'.format(self.name, self.slug)


class Title(models.Model):
    """Ресурс Title"""
    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.IntegerField(
        validators=[
            year_validator
        ],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            )
        ]
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return '{} ({} г.): {}, {}. Описание: {}'.format(
            self.name, self.year, self.category.slug,
            self.genre.slug, self.description[:15]
        )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review_titles',
        help_text='Оцениваемое произведение',
    )
    text = models.TextField(
        'Текст обзора',
        help_text='Текст обзора')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Автор отзыва',
    )
    score = models.IntegerField(
        'Оценка произведения',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
    )
    pub_date = models.DateTimeField(
        'Дата и время написания обзора',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='only_one_review_on_author'
            )
        ]

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    """Ресурс Comments."""

    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment',
        help_text='Комментарий к обзору')
    text = models.TextField(
        'Текст комментария',
        help_text='Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата и время написания комментария',
        auto_now_add=True
    )

    class Meta:

        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
