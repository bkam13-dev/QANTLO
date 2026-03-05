from django.shortcuts import render
from rest_framework import generics
from apps.suppliers.serializers import SupplierSerializers
from apps.suppliers.models import Supplier

# Create your views here.

class CreateSupplierView(generics.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    
class ListSupplierView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    
class RetrieveSupplierView(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    
class DestroySupplierView(generics.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    

    
