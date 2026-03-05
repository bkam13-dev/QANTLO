from rest_framework import serializers
from apps.inventory.models import Product, StockMovement, Category
from django.db.models import F

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)
    image = serializers.ImageField(required=False, allow_null=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'sku', 'price', 'quantity', 'image','category', 'is_active','created_at' ]
        read_only_fields = ['id', 'slug', 'sku', 'created_at']
     
         
   
        
class StockMovementSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=0)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = StockMovement
        fields = ['id', 'movement', 'product', 'quantity', 'supplier', 'created_at', 'created_by']  
        read_only_fields = ['id', 'created_at', 'created_by']


    def validate(self, attrs):
        if attrs['movement'] == 'OUT':
            product = attrs['product']
            quantity = attrs['quantity']
            
            instance = self.instance
            available = product.quantity
            if instance and instance.movement == 'OUT':
                available += instance.quantity
            
            if product.quantity < quantity:
                raise serializers.ValidationError({
                    'quantity': f"quantité insuffisante en stock, le stock actuel est {product.quantity}"
                })
        return super().validate(attrs)


    def create(self, validated_data):
        movement = validated_data['movement']
        product = validated_data['product']
        quantity = validated_data['quantity']
        
        if movement == 'IN':
            Product.objects.filter(pk=product.id).update(quantity=F('quantity') + quantity)
        else:
            Product.objects.filter(pk=product.id).update(quantity=F('quantity') - quantity)
        return super().create(validated_data)
    
    
    def update(self, instance, validated_data):
        movement = validated_data['movement']
        product = validated_data['product']
        quantity = validated_data['quantity']
        
        if instance.movement == 'IN':
            Product.objects.filter(pk=instance.product.id).update(quantity=F('quantity') - instance.quantity)
        else:
            Product.objects.filter(pk=instance.product.id).update(quantity=F('quantity') + instance.quantity)

        if movement == 'IN':
            Product.objects.filter(pk=product.id).update(quantity=F('quantity') + quantity)
        else:
            Product.objects.filter(pk=product.id).update(quantity=F('quantity') - quantity)
        
        return super().update(instance, validated_data)
    
    

class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
        