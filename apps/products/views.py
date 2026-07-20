from django.shortcuts import render
from apps.products.models import Product, Category, Supplier, Brand
from apps.products.serializers import ProductSerializer, CategorySerializer, SupplierSerializer, BrandSerializer
from rest_framework import viewsets

# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    

class SupplierViewset(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
    
class BrandViewset(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    
    
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').select_related('supplier').select_related('brand').all()
    serializer_class = ProductSerializer