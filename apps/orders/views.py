from django.shortcuts import render
from rest_framework import viewsets
from apps.orders.models import Order, OrderItem, Invoice
from apps.orders.serializers import OrderSerializer, OrderItemSerializer, DetailOrderItemSerializer, InvoiceSerializer, DetailOrderSerializer


# Create your views here.


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('supplier').select_related('created_by').all()
    
    def get_serializer_class(self):
        if (self.action) not in ['list', 'retrieve']:
            return OrderSerializer
        return DetailOrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order').select_related('product').all()
    
    def get_serializer_class(self):
        if self.action not in ['list', 'retrieve']:
            return OrderItemSerializer
        return DetailOrderItemSerializer
    
        
class InvoiceViewset(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('order').prefetch_related('order__items__product').all()
    serializer_class = InvoiceSerializer