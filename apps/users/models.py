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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(unique= True, max_length=150)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STAFF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    

# model Profil Utilisateur
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile de {self.user.username}"
    