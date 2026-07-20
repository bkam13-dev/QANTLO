from django.db import models
from apps.products.models import Product
from apps.users.models import CustomUser
import uuid

# Create your models here.

# model entrepôt
class WareHouse(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    

# model article en stock
class StockItem(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name="stock_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} : {self.quantity}"
    


# model mouvement de stock
class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', 'Entrée'
        OUT = 'OUT', 'Sortie'
        ADJUSTMENT = 'ADJUSTMENT', 'Ajustement'
    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name="stock_movements")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices, default=MovementType.IN)
    quantity = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='movements')
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.movement_type} - {self.item.product.name} : {self.quantity}"