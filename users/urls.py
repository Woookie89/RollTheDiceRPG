from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import (CustomUserViewSet)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('register/', CustomUserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', CustomUserViewSet.as_view({'post': 'login'}), name='login'),
    path('profile/', CustomUserViewSet.as_view({'get': 'profile'}), name='profile'),
    path('profile/edit/', CustomUserViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='edit_profile'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
