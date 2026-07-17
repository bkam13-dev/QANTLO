from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


# model utilisateur
class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrateur'
        MANAGER = 'MANAGER', 'Manager'
        STAFF = 'STAFF', 'Staff'
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    role = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STAFF)
    
    

# model Profil Utilisateur
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    phone = models.CharField(max_length=20, blank=True)
    
    