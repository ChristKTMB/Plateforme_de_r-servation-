from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from apps.core.models import TimeStampedModel

class User(AbstractUser):
    """Utilisateurs personalisé"""
    USER_TYPE_CHOICES = (
        ("C", "Client"),
        ("O", "Organisateur"),
        ("A", "Administrateur"),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default="C")
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profils', blank=True)

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
