from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'register', views.RegistrationViewSet, basename='register')
router.register(r'users', views.CustomUserViewSet)

app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
]
