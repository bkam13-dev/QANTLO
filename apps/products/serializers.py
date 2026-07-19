from rest_framework import serializers
from apps.products.models import Product, Brand, Category, Supplier




# Serializer du model Catégorie
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']
        read_only_fields = ['id', 'slug']
        
        

# Serializer du model Marque
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
        
        

# Serializer du model Fournisseur
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'company_name', 'contact_name', 'email', 'phone', 'address']
        read_only_fields = ['id']
       
        

# Serializer du model Produit
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    supplier = SupplierSerializer()
    class Meta:
        model = Product
        fields = ['id', 'category', 'brand', 'supplier', 'sku', 'barcode', 'name', 'slug', 'description', 'purchase_price', 'selling_price', 'min_stock_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sku', 'barcode', 'slug', 'created_at', 'updated_at']
