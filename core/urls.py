"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.inventory.views import WareHouseViewset, StockItemViewset, StockMovementViewset
from apps.products.views import ProductViewset, BrandViewset, SupplierViewset, CategoryViewset
from apps.orders.views import OrderViewset, OrderItemViewset, InvoiceViewset
from apps.users.views import CustomUserViewset, UserProfileViewset


router = DefaultRouter()
router.register(r"users", CustomUserViewset, basename="user")
router.register(r"profiles", UserProfileViewset, basename="profile")
router.register(r"categories", CategoryViewset, basename="category")
router.register(r"suppliers", SupplierViewset, basename="supplier")
router.register(r"brands", BrandViewset, basename="brand")
router.register(r"products", ProductViewset, basename="product")
router.register(r"orders", OrderViewset, basename="order")
router.register(r"order_items", OrderItemViewset, basename="order_item")
router.register(r"invoices", InvoiceViewset, basename="invoice")
router.register(r"warehouses", WareHouseViewset, basename="warehouse")
router.register(r"stock_items", StockItemViewset, basename="stock_item")
router.register(r"stock_movements", StockMovementViewset, basename="stock_movement")




urlpatterns = [
    path('admin/', admin.site.urls),
]
