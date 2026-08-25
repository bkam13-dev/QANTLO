import re

from django.db import models
import uuid
from django.utils.text import slugify

# Create your models here.

# model Catégorie
class Category(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
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
    
class Customer(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    company_name = models.CharField(max_length=255, null=True , blank=True)
    contact_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    def __str__(self):
        if self.company_name is not None:
            return self.company_name 
        return f"{self.first_name}  {self.last_name}"


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
    sku_number = models.PositiveIntegerField(unique=True, editable=False, null=True)
    sku = models.CharField(unique=True, max_length=255, null=False, blank=True)
    barcode = models.CharField(unique=True, null=True, blank=True, max_length=255)
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=True)
    description = models.TextField(blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    min_stock_level = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    # fonction qui génère le sku
    def generate_sku(self):
        
        category_code = re.sub(r'[^A-Z]', '', self.category.name.upper())[:3] if self.category else 'GEN'
        category_code = category_code or 'GEN'

        brand_code = re.sub(r'[^A-Z]', '', self.brand.upper())[:3] if self.brand else 'GEN'
        brand_code = brand_code or 'GEN'

        if not self.sku_number:
            last_num = Product.objects.aggregate(models.Max('sku_number'))['sku_number__max']
            self.sku_number = (last_num or 0) + 1

        id_code = f"{self.sku_number:06d}"

        return f"{category_code}-{brand_code}-{id_code}"
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if not self.sku:
            self.sku = self.generate_sku()
        
        return super().save(*args, **kwargs)
    

