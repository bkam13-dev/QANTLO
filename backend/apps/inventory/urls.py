from django.urls import path, include
from apps.inventory.views import CreateProductView, ListProductView, RetrieveProductView, DestroyProductView, CreateStockMovementView, ListStockMovementView, DestroyStockMovementView, RetrieveStockMovementView, CreateCategoryView, ListCategoryView, RetrieveCategoryView, DestroyCategoryView
urlpatterns = [
    
    path('products/list/', ListProductView.as_view()),
    path('products/create/', CreateProductView.as_view()),
    path('products/<slug:slug>/', RetrieveProductView.as_view()),
    path('products/<slug:slug>/delete/', DestroyProductView.as_view()),
    path('stockmovement/list/', ListStockMovementView.as_view()),
    path('stockmovement/create/', CreateStockMovementView.as_view()),
    path('stockmovement/<uuid:id>/', RetrieveStockMovementView.as_view()),
    path('stockmovement/<uuid:id>/delete/', DestroyStockMovementView.as_view()),
    path('category/list/', ListCategoryView.as_view()),
    path('category/create/', CreateCategoryView.as_view()),
    path('category/<slug:slug>/', RetrieveCategoryView.as_view()),
    path('category/<slug:slug>/delete/', DestroyCategoryView.as_view()),
]
