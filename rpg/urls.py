from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('campaigns/new/', views.campaign_create, name='campaign-create'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign-detail'),
    path('characters/new/', views.character_create, name='character-create'),
    path('characters/<int:pk>/', views.character_detail, name='character-detail'),
    path('characters/<int:pk>/edit/', views.character_edit, name='character-edit'),
    path('rolls/new/', views.roll_create, name='roll-create'),
    path('journal/new/', views.journal_create, name='journal-create'),
]
