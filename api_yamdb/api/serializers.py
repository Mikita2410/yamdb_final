from rest_framework import serializers
from django.shortcuts import get_object_or_404

from api_yamdb.settings import (USERNAME_MAX_LENGTH,
                                CONFIRMATION_CODE_MAX_LENGTH,
                                EMAIL_MAX_LENGTH)
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = fields


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'Нельзя оставить отзыв на одно произведение дважды.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта 'users/' для пользователя с ролью 'admin'."""

    def validate_username(self, username):
        return validate_username(username)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserSerializer(UserAdminSerializer):
    """Сериализатор для эндпоинта 'users/me/'."""

    class Meta(UserAdminSerializer.Meta):
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для эндпоинта 'auth/token' для всех пользователей."""
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=CONFIRMATION_CODE_MAX_LENGTH
    )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для эндпоинта 'auth/signup' для всех пользователей."""

    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(required=True, max_length=EMAIL_MAX_LENGTH)
