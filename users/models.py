from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(models.Model):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    favourites = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.username
