from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (CategoryViewSet, GenreViewSet, sign_up,
                    GetTokenApiView, TitleViewSet,
                    UserViewSet, CommentViewSet,
                    ReviewViewSet)

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', GetTokenApiView.as_view(), name='gen_access_token')
]
