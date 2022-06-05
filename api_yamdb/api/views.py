from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api_yamdb.settings import EMAIL_ADRESS

from .mixins import CreateDestroyListViewSet
from .paginations import CommentSetPagination, ReviewsSetPagination
from .permissions import (AdminModeratorAuthorOrReadOnly, IsAdminOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetConfirmationCodeSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          TitleCreateUpdateDeleteSerializer,
                          TitleReadSerializer, UserForAdminSerializer,
                          UserSerializer)

from. filters import TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет Отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = ReviewsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AdminModeratorAuthorOrReadOnly,
                          )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review_titles.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет Комментов"""
    serializer_class = CommentSerializer
    pagination_class = CommentSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title=title_id, pk=review_id)
        return review.comment.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title=title_id, pk=review_id)
        serializer.save(author=self.request.user, review_id=review)


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет Категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет Жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет оглавлений."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    queryset = Title.objects.annotate(
        rating=Avg('review_titles__score')
    ).order_by('pk')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        else:
            return TitleCreateUpdateDeleteSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Юзера."""
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = (IsAdminOnly, permissions.IsAuthenticated)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['PATCH', 'GET'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request, ):
        serializer = UserSerializer(request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenApiView(APIView):
    """Вьюсет обработки токенов."""
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            access_token = RefreshToken.for_user(user).access_token
            data = {'token': str(access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        errors = {'error': 'confirmation code incorrect'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def sign_up(request):
    """Генратор кода подтверждения."""
    serializer = GetConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject=EMAIL_ADRESS,
        message=confirmation_code,
        from_email=EMAIL_ADRESS,
        recipient_list=(user.email,)
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
