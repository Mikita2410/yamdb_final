from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import (
    USERNAME_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    TYPOLOGIES_NAME_MAX_LENGTH,
    TYPOLOGIES_SLUG_MAX_LENGTH
)
from reviews.validators import validate_year, validate_username


class User(AbstractUser):
    """Модель для Юзера."""
    class RoleChoices(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        unique=False, blank=True)
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        unique=False, blank=True)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        max_length=max(len(role) for role, _ in RoleChoices.choices)
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == User.RoleChoices.ADMIN
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return (
            self.role == User.RoleChoices.MODERATOR
        )


class Typologies(models.Model):
    name = models.CharField(
        max_length=TYPOLOGIES_NAME_MAX_LENGTH,
        db_index=True
    )
    slug = models.SlugField(
        max_length=TYPOLOGIES_SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(Typologies):
    """Категории произведений."""

    class Meta(Typologies.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(Typologies):
    """Жанры произведений."""

    class Meta(Typologies.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=TYPOLOGIES_NAME_MAX_LENGTH,
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год произведения',
        validators=(validate_year, )
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения'
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Feedback(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return (self.text)[:15]


class Review(Feedback):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta(Feedback.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_combination'
            )
        ]


class Comment(Feedback):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(Feedback.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
