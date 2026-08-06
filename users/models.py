from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    PLAYER = 'player'
    GAME_MASTER = 'game_master'

    PROFILE_ROLE_CHOICES = [
        (PLAYER, 'Gracz'),
        (GAME_MASTER, 'Mistrz Gry'),
    ]

    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    profile_role = models.CharField(max_length=24, choices=PROFILE_ROLE_CHOICES, default=PLAYER)

    def __str__(self):
        return self.username

    @property
    def is_game_master(self):
        return self.profile_role == self.GAME_MASTER
