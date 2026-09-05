from django.shortcuts import render
from apps.products.models import Product, Category, Supplier, Brand
from apps.products.serializers import ProductSerializer, DetailProductSerializer, TreeCategorySerializer, FlatCategorySerializer, DetailCategorySerializer, SupplierSerializer, BrandSerializer
from rest_framework import viewsets

# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.request.query_params.get('tree') == "true":
            return TreeCategorySerializer
        if self.action == 'retrieve':
            return DetailCategorySerializer
        return FlatCategorySerializer  
    

class SupplierViewset(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
    
class BrandViewset(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    
    
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').select_related('supplier').select_related('brand').all()
    
    def get_serializer_class(self):
        if (self.action) not in ['list', 'retrieve']:
            return ProductSerializer
        return DetailProductSerializer