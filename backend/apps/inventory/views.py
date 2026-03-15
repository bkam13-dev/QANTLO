from django.shortcuts import render
from rest_framework import generics
from apps.inventory.models import Product, StockMovement, Category
from apps.inventory.serializers import ProductSerializer, StockMovementSerializer, CategorySerializer
from django.db.models import Count, Avg
from rest_framework.response import Response
from rest_framework import permissions
from core.permissions import IsAdmin, IsManager, IsStaff

# Les vues du model Product
class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]
    
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
    permission_classes = [permissions.IsAuthenticated, IsManager]
   
    
class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    
    
class DestroyProductView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsManager]
   
 
   
# Les vues du model StockMovement
    
class CreateStockMovementView(generics.CreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]


class ListStockMovementView(generics.ListAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]

  
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
    permission_classes = [permissions.IsAuthenticated, IsStaff]


class DestroyStockMovementView(generics.DestroyAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsManager]



# Les vues du model Category

class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]
    
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
    permission_classes = [permissions.IsAuthenticated, IsManager]
  
    
class RetrieveCategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    
class DestroyCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsManager]
