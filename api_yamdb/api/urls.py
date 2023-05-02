from django.urls import include, path
from rest_framework.routers import DefaultRouter


from api.views import (
    UserViewSet, TitleViewSet,
    CategoryViewSet, GenreViewSet,
    ReviewViewSet, CommentViewSet,
    SignUpView, GetTokenView
)


router_ver1 = DefaultRouter()
router_ver1.register('users', UserViewSet, basename='users')
router_ver1.register('titles', TitleViewSet, basename='titles')
router_ver1.register('categories', CategoryViewSet, basename='categories')
router_ver1.register('genres', GenreViewSet, basename='genres')
router_ver1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_ver1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('auth/signup/', SignUpView.as_view()),
    path('auth/token/', GetTokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(router_ver1.urls)),
    path('v1/', include(auth_urls)),
]
