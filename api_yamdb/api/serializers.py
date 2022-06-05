from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .utils import validate_username


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if (self.context['view'].request.method == 'POST'
                and title.review_titles.filter(
                    author=self.context['request'].user).exists()):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение.')
        return data

    class Meta:
        model = Review

        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Комментов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категорий."""

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров."""
    class Meta:
        model = Genre
        exclude = ['id']


class TitleCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    """Сериализатор создания, редактирования и удаления Оглавлений"""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = ('__all__')

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения Оглавлений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('__all__')


class UserForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор Юзера и Админа."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Юзера."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        read_only_fields = ('role', 'email')
        validations = [validate_username]


class GetConfirmationCodeSerializer(serializers.ModelSerializer):
    """Сериализатор Аутентификации."""
    username = serializers.CharField(
        max_length=150,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == settings.USER_ME:
            raise serializers.ValidationError(
                'Для имени нельзя использовать {value}'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор обработки токенов."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
