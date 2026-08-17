from rest_framework import serializers
from apps.products.models import Product, Brand, Category, Supplier




# Serializer du model Catégorie
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon_name', 'is_active', 'display_order']
        read_only_fields = ['id', 'slug']
        

class CategorySerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True, read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon_name', 'is_active', 'display_order', 'parent', 'parent_name', 'children']
        read_only_fields = ['id', 'slug']
        
        
class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon_name', 'is_active', 'display_order', 'parent']
        read_only_fields = ['id', 'slug']

    def validate_parent(self, value):
        if self.instance and value == self.instance:
            raise serializers.ValidationError("Une catégorie ne peut pas être son propre parent.")        
        return value
    
    

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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(is_active=True))
    category_details = CategorySerializer(source='category', read_only=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), allow_null=False, required=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), allow_null=False, required=True)
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_details', 'brand', 'brand_name', 'supplier', 'supplier_name', 'sku', 'barcode', 'name', 'slug', 'description', 'purchase_price', 'selling_price', 'min_stock_level', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id','supplier_name', 'brand_name', 'sku', 'barcode', 'slug', 'created_at', 'updated_at']
