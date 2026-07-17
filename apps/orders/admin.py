from django.contrib import admin
from apps.orders.models import Order, OrderItem, Invoice
# Register your models here.



# rendu du model Order dans django admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


# rendu du model OrderItem dans django admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass



# rendu du model Invoice dans django admin
@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    pass
