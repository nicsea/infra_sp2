from django.urls import path

from rest_framework.routers import DefaultRouter

from api.v1.views import CategoryViewSet, CommentViewSet, GenreViewSet, \
    TitleViewSet, ReviewViewSet
from users.views import UserSignupAPIView, GetTokenView, UserViewSet, MeAPIView


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

reviews_path = r'titles/(?P<title_id>\d+)/reviews'
router.register(reviews_path, ReviewViewSet, basename='reviews')
router.register(reviews_path + r'/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('users/me/', MeAPIView.as_view()),
    path('auth/signup/', UserSignupAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenView.as_view(), name='get_token'),
]

urlpatterns += router.urls
