from rest_framework import serializers
from django.shortcuts import get_object_or_404
from apps.inventory.models import WareHouse, StockItem, StockMovement
from apps.products.models import Product
from apps.users.serializers import CustomUserSerializer
from apps.users.models import CustomUser
from apps.products.serializers import ProductSerializer, DetailProductSerializer


# Serializer du model Entrepôt
class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['id', 'name', 'address']
        read_only_fields = ['id']
        
        
        
        
# Serializer du model Article en stock        
class StockItemSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=WareHouse.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.select_related('category').select_related('brand').select_related('supplier').all())
    class Meta:
        model = StockItem
        fields = ['id', 'warehouse', 'product', 'quantity']
        read_only_fields = ['id']


class DetailStockItemSerializer(serializers.ModelSerializer):
    warehouse = serializers.StringRelatedField()
    product = DetailProductSerializer()
    class Meta:
        model = StockItem
        fields = ['id', 'warehouse', 'product', 'quantity']
        read_only_fields = ['id']
        
        
        
        
# Serializer du model Mouvement de stock      
class StockMovementSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=StockItem.objects.select_related('warehouse').select_related('product').all())
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'item', 'movement_type', 'quantity', 'user', 'reason', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class DetailStockMovementSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    user = CustomUserSerializer()
    class Meta:
        model = StockMovement
        fields = ['id', 'item', 'movement_type', 'quantity', 'user', 'reason', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']