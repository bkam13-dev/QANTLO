from django.shortcuts import render
from rest_framework import generics
from apps.inventory.models import Product, StockMovement, Category
from apps.inventory.serializers import ProductSerializer, StockMovementSerializer, CategorySerializer
from django.db.models import Count, Avg
from rest_framework.response import Response


# Les vues du model Product
 
class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'countProduct': queryset.count(),
            'results': serializer.data,
        })
        
        
class CreateProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    
    
class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    
    
class DestroyProductView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
   
 
   
# Les vues du model StockMovement
    
class CreateStockMovementView(generics.CreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer


class ListStockMovementView(generics.ListAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'countStockMovement': queryset.count(),
            'results': serializer.data,
        })
    
    
class RetrieveStockMovementView(generics.RetrieveAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    lookup_field = 'id'


class DestroyStockMovementView(generics.DestroyAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    lookup_field = 'id'



# Les vues du model Category

class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'countProduct': queryset.count(),
            'results': serializer.data,
        })
        
        
class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer    
    
    
class RetrieveCategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    
class DestroyCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'