from django.shortcuts import render
from rest_framework import generics
from apps.suppliers.serializers import SupplierSerializers
from apps.suppliers.models import Supplier
from rest_framework import permissions
from core.permissions import IsAdmin, IsManager, IsStaff


class CreateSupplierView(generics.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    permission_classes = [permissions.IsAuthenticated, IsManager]
    
class ListSupplierView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    permission_classes = [permissions.IsAuthenticated, IsStaff]
  
class RetrieveSupplierView(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    permission_classes = [permissions.IsAuthenticated, IsStaff]
   
class DestroySupplierView(generics.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    permission_classes = [permissions.IsAuthenticated, IsManager]


    
