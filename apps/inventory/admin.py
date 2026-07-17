from django.contrib import admin
from apps.inventory.models import WareHouse, StockItem, StockMovement
# Register your models here.

# rendu du model WareHouse dans django admin
@admin.register(WareHouse)
class WareHouseAdmin(admin.ModelAdmin):
    pass


# rendu du model StockItem dans django admin
@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    pass




# rendu du model StockMovement dans django admin
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    pass