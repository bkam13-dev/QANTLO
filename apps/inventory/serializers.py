from rest_framework import serializers
from apps.inventory.models import WareHouse, StockItem, StockMovement
from apps.users.serializers import CustomUserSerializer
from apps.products.serializers import ProductSerializer


# Serializer du model Entrepôt
class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['id', 'name', 'address']
        read_only_fields = ['id']
        
        
        
        
# Serializer du model Article en stock        
class StockItemSerializer(serializers.ModelSerializer):
    warehouse = WareHouseSerializer()
    product = ProductSerializer()
    class Meta:
        model = StockItem
        fields = ['id', 'warehouse', 'product', 'quantity']
        read_only_fields = ['id']
        
        
        
        
# Serializer du model Mouvement de stock      
class StockMovementSerializer(serializers.ModelSerializer):
    item = StockItemSerializer()
    user = CustomUserSerializer()
    class Meta:
        model = StockMovement
        fields = ['id', 'item', 'movement_type', 'quantity', 'user', 'reason', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
