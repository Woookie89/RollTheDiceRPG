from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('campaigns/new/', views.campaign_create, name='campaign-create'),
    path('characters/new/', views.character_create, name='character-create'),
    path('rolls/new/', views.roll_create, name='roll-create'),
]
