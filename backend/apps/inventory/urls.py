from django.urls import path, include
from apps.inventory.views import CreateProductView, ListProductView, RetrieveProductView, DestroyProductView, CreateStockMovementView, ListStockMovementView, DestroyStockMovementView, RetrieveStockMovementView, CreateCategoryView, ListCategoryView, RetrieveCategoryView, DestroyCategoryView
urlpatterns = [
    
    path('products/', ListProductView.as_view()),
    path('products/new/', CreateProductView.as_view()),
    path('products/<slug:slug>/', RetrieveProductView.as_view()),
    path('products/<slug:slug>/', DestroyProductView.as_view()),
    path('stockmovement/', ListStockMovementView.as_view()),
    path('stockmovement/new/', CreateStockMovementView.as_view()),
    path('stockmovement/<uuid:id>/', RetrieveStockMovementView.as_view()),
    path('stockmovement/<uuid:id>/', DestroyStockMovementView.as_view()),
    path('category/', ListCategoryView.as_view()),
    path('category/new/', CreateCategoryView.as_view()),
    path('category/<slug:slug>/', RetrieveCategoryView.as_view()),
    path('category/<slug:slug>/', DestroyCategoryView.as_view()),
]
