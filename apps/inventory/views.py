from django.shortcuts import render
from rest_framework import viewsets
from apps.inventory.models import WareHouse, StockItem, StockMovement
from apps.inventory.models import WareHouse, StockItem, StockMovement
from apps.inventory.serializers import WareHouseSerializer, StockItemSerializer, StockMovementSerializer, DetailStockItemSerializer, DetailStockMovementSerializer

# Create your views here.



class WareHouseViewset(viewsets.ModelViewSet):
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseSerializer
 
    
    
class StockItemViewset(viewsets.ModelViewSet):
    queryset = StockItem.objects.select_related('product').select_related('warehouse').all()
    
    def get_serializer_class(self):
        if(self.action) not in ['list', 'retrieve']:
            return StockItemSerializer
        return DetailStockItemSerializer
    

    
    
    
class StockMovementViewset(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related('item__product', 'item__warehouse').select_related('user').all()

    def get_serializer_class(self):
        if(self.action) not in ['list', 'retrieve']:
            return StockMovementSerializer
        return DetailStockMovementSerializer
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
