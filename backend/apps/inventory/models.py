from django.db import models
from django.utils.text import slugify
from core.utils import generate_sku
from django.contrib.auth import get_user_model
from apps.suppliers.models import Supplier
import uuid


User = get_user_model()


class Category(models.Model):        
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        
class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categorie_product', verbose_name='categories')
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
     
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = generate_sku()
        super().save(*args, **kwargs)
        
        
    

class StockMovement(models.Model):
    class MOVEMENT_TYPE(models.TextChoices):
        IN = 'IN', 'In'
        OUT = 'OUT', 'Out'
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    movement = models.CharField(choices=MOVEMENT_TYPE, default=MOVEMENT_TYPE.IN)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='stockMovement_products', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='stockMovement_supplier')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='stockMovement_creator', null=True, blank=True)
    
    def __str__(self):
        return f" {self.quantity} {self.product_id.name} {self.movement} stock"
    
    