from django.contrib import admin
from apps.products.models import Category, Product, Supplier, Brand
# Register your models here.



# rendu du model Category dans django admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass



# rendu du model Product dans django admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass




# rendu du model Supplier dans django admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass




# rendu du model Brand dans django admin
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass