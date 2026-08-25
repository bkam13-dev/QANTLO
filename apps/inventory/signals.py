from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from apps.inventory.models import StockItem, StockMovement


@receiver(post_save, sender=StockMovement)
def adding_or_removing_product_quantity(sender, instance, created, **kwargs):
    if not created:
        return
    
    with transaction.atomic():
        stock_item = (StockItem.objects.select_for_update().get(pk=instance.item_id))
        
        if instance.movement_type == StockMovement.MovementType.IN:
            stock_item.quantity += instance.quantity
            
        elif instance.movement_type == StockMovement.MovementType.OUT:
            if stock_item.quantity < instance.quantity:
                raise ValueError("La quantité en entrepôt est insuffisante pour cette opération")
            stock_item.quantity -= instance.quantity
        
        stock_item.save(update_fields=['quantity'])
        