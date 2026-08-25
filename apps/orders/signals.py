from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from apps.orders.models import Order, Invoice
    
    
    
@receiver(post_save, sender=Order)
def create_invoice(sender, instance, created, **kwargs):
    if instance.status != Order.StatusChoice.COMPLETED:
        return
    with transaction.atomic():
        invoice, invoice_created = Invoice.objects.get_or_create(order=instance)
        total = sum(
            item.total_amount_item
            for item in instance.items.all()
        )
        invoice.total_amount = total
        invoice.save()