from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    class ROLE_CHOICE(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        STAFF = 'STAFF','Staff' 
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    role = models.CharField(choices=ROLE_CHOICE, default=ROLE_CHOICE.STAFF)
    created_at = models.DateTimeField(auto_now=True)
    

