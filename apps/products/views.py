from django.shortcuts import render
from apps.products.models import Product, Category, Supplier, Brand
from apps.products.serializers import ProductSerializer, CategorySerializer, SubCategorySerializer, CategoryCreateUpdateSerializer, SupplierSerializer, BrandSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer
    
    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True).prefetch_related("children")
        parent_id = self.request.query_params.get('parent_id')
        if parent_id is not None:
            if(parent_id.lower() == 'null'):
                return queryset.filter(parent__isnull=True)
            return queryset.filter(parent_id=parent_id)
        return queryset
    
    @action(detail=False, methods=['get'], url_path='main_categories')
    def main_categories(self, request):
        main_categories = self.get_queryset().filter(parent__isnull=True)   
        serializer = CategorySerializer(main_categories, many=True)    
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SupplierViewset(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
    
class BrandViewset(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    
    
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').select_related('supplier').select_related('brand').all()
    serializer_class = ProductSerializer