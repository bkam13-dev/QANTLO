from django.db import models
from products.models import Supplier, Product
from users.models import CustomUser
import uuid

# Create your models here.

# model commande
class Order(models.Model):
    
    class OrderType(models.TextChoices):
        PURCHASE = 'PURCHASE', 'Achat fournisseur'
        SALE = 'SALE', 'Vente client'
        
    class StatusChoice(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        PROCESSING = 'PROCESSING', 'En cours de traitement'
        COMPLETED = 'COMPLETED', 'Terminée'
        CANCELLED = 'CANCELLED', 'Annulée'
        
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.PURCHASE)
    status = models.CharField(max_length=20, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    reference = models.CharField(max_length=255, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    created_by = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"${self.order_type} - ${self.reference} - ${self.status}"
    

# model article de commande
class OrderItem(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"${self.product.name} : ${self.quantity} - ${self.unit_price } Fcfa"


# model facture
class Invoice(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoices")
    total_amount = models.DecimalField(decimal_places=2)
    is_paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"${self.total_amount} - ${self.is_paid} - ${self.order.status}"
