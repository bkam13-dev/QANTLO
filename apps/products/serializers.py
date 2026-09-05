from rest_framework import serializers
from apps.products.models import Product, Brand, Category, Supplier, Customer




# Serializer du model Catégorie
class FlatCategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']
        read_only_fields = ['id', 'slug']
        
    def validate_parent(self, value):
        if self.instance and value == self.instance:
            raise serializers.ValidationError('Une catégorie ne peut pas être son propre parent')
        return value

class TreeCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = FlatCategorySerializer()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children']
        read_only_fields = ['id', 'slug']

    def get_children(self, obj):
        if obj.children.exists():
            return TreeCategorySerializer(obj.children.all(), many=True).data
        return []

class DetailCategorySerializer(serializers.ModelSerializer):
    children = TreeCategorySerializer(source='children.all', many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children']
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
       
        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'company_name', 'contact_name', 'first_name', 'last_name', 'email', 'phone', 'address']
        read_only_fields = ['id']



# Serializer du model Produit
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    class Meta:
        model = Product
        fields = ['id', 'category', 'brand', 'supplier', 'sku', 'barcode', 'name', 'slug', 'description', 'purchase_price', 'selling_price', 'min_stock_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sku', 'barcode', 'slug', 'created_at', 'updated_at']


class DetailProductSerializer(serializers.ModelSerializer):
    category = FlatCategorySerializer()
    brand = BrandSerializer()
    supplier = SupplierSerializer()
    class Meta:
        model = Product
        fields = ['id', 'category', 'brand', 'supplier', 'sku', 'barcode', 'name', 'slug', 'description', 'purchase_price', 'selling_price', 'min_stock_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sku', 'barcode', 'slug', 'created_at', 'updated_at']