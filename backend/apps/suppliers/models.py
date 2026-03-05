from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.

class Supplier(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True, null=True, verbose_name='contact')
    is_active = models.BooleanField(default=True, verbose_name='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}  -  contact: {self.phone}"
