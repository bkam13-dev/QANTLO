from django.db import models
import uuid
from django.utils.text import slugify

# Create your models here.

# model Catégorie
class Category(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


# model fournisseur
class Supplier(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    def __str__(self):
        return self.company_name
    


# model Marque
class Brand(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name



# model Produit
class Product(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_list")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="products_supplied")
    sku = models.CharField(unique=True, max_length=255, null=False)
    barcode = models.CharField(unique=True, null=False, blank=True, max_length=255)
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock_level = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    

