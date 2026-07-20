from django.shortcuts import render
from rest_framework import viewsets
from apps.orders.models import Order, OrderItem, Invoice
from apps.orders.serializers import OrderSerializer, OrderItemSerializer, InvoiceSerializer


# Create your views here.


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('supplier').select_related('created_by').all()
    serializer_class = OrderSerializer
    
    
class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order').select_related('product').all()
    serializer_class = OrderItemSerializer
    
    
    
class InvoiceViewset(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('order').all()
    serializer_class = InvoiceSerializer