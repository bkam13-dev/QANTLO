from rest_framework import serializers
from apps.orders.models import Order, OrderItem, Invoice
from apps.products.serializers import ProductSerializer, SupplierSerializer
from apps.products.models import Product, Supplier
from apps.users.serializers import CustomUserSerializer



# Serializer du model Article de commande
class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.select_related('created_by').all(), allow_null=False, required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.select_related('category').select_related('supplier').select_related('brand').all())
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']
        read_only_fields = ['id']




# Serializer du model Commande
class OrderSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), allow_null=False, required=True)
    created_by = CustomUserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_type', 'order_items', 'status', 'reference', 'supplier', 'created_by', 'created_at']
        read_only_fields = ['id', 'reference', 'created_by', 'created_at']
        
              
        
        
# Serializer du model Facture
class InvoiceSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'total_amount', 'is_paid', 'issued_at']
        read_only_fields = ['id', 'total_amount', 'issued_at']
        