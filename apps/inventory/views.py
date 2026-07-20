from django.shortcuts import render
from rest_framework import viewsets
from apps.inventory.models import WareHouse, StockItem, StockMovement
from apps.inventory.models import WareHouse, StockItem, StockMovement
from apps.inventory.serializers import WareHouseSerializer, StockItemSerializer, StockMovementSerializer

# Create your views here.



class WareHouseViewset(viewsets.ModelViewSet):
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseSerializer
 
    
    
class StockItemViewset(viewsets.ModelViewSet):
    queryset = StockItem.objects.select_related('product').select_related('warehouse').all()
    serializer_class = StockItemSerializer
    
    
    
class StockMovementViewset(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related('item__product', 'item__warehouse').select_related('users').all()
    serializer_class = StockMovementSerializer
    
    
    