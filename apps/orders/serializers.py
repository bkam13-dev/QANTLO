from rest_framework import serializers
from apps.orders.models import Order, OrderItem, Invoice
from apps.products.models import Supplier, Product, Customer
from apps.products.serializers import ProductSerializer, SupplierSerializer
from apps.users.serializers import CustomUserSerializer



# Serializer du model Article de commande
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.select_related('category').select_related('brand').select_related('supplier').all())
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']
        read_only_fields = ['id']
  
  
        
class DetailOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']
        read_only_fields = ['id']
        


# Serializer du model Commande
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False, allow_null=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_type', 'items', 'status', 'reference', 'supplier', 'customer', 'created_by', 'created_at']
        read_only_fields = ['id', 'reference', 'created_by', 'created_at']
      
    def validate_items(self, value):
        if not value or len(self.items) == 0:
            raise serializers.ValidationError("Une commande doit contenir au moins un article.")
        return value
            
                
        
class DetailOrderSerializer(serializers.ModelSerializer):
    items = DetailOrderItemSerializer(many=True, read_only=True)
    supplier = SupplierSerializer(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_type', 'items', 'status', 'reference', 'supplier', 'created_by', 'created_at']
        read_only_fields = ['id', 'reference', 'created_by', 'created_at']
        
        
      
# Serializer du model Facture
class InvoiceSerializer(serializers.ModelSerializer):
    order = DetailOrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order')
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'order_id', 'total_amount', 'is_paid', 'issued_at']
        read_only_fields = ['id', 'total_amount', 'issued_at']
        