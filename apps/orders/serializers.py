from rest_framework import serializers
from apps.orders.models import Order, OrderItem, Invoice
from apps.products.serializers import ProductSerializer, SupplierSerializer
from apps.users.serializers import CustomUserSerializer


# Serializer du model Commande
class OrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    created_by = CustomUserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_type', 'status', 'reference', 'supplier', 'created_by', 'created_at']
        read_only_fields = ['id', 'reference', 'created_by', 'created_at']
        
        
        
# Serializer du model Article de commande
class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']
        read_only_fields = ['id']
        
        
        
# Serializer du model Facture
class InvoiceSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'total_amount', 'is_paid', 'issued_at']
        read_only_fields = ['id', 'total_amount', 'issued_at']
        