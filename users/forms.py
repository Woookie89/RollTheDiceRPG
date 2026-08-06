from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'avatar', 'profile_role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar', 'first_name', 'last_name', 'profile_role', 'password')


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'profile_role')
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Email',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'avatar': 'Avatar',
            'profile_role': 'Rola przy stole',
        }
