from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import CustomUserViewSet, RegisterView, profile_view

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/', profile_view, name='profile'),
    path('register/', CustomUserViewSet.as_view({'post': 'register'}), name='api-register'),
    path('login/', CustomUserViewSet.as_view({'post': 'login'}), name='api-login'),
    path('profile/', CustomUserViewSet.as_view({'get': 'profile'}), name='api-profile'),
    path('profile/edit/', CustomUserViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='api-edit-profile'),
    path('users/profile/', CustomUserViewSet.as_view({'get': 'profile'}), name='api-user-profile'),
    path('users/profile/edit/', CustomUserViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='api-user-edit-profile'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
