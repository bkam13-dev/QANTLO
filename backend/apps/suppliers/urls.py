from django.urls import path, include
from apps.suppliers.views import CreateSupplierView, ListSupplierView, DestroySupplierView, RetrieveSupplierView

urlpatterns = [
    path('/', ListSupplierView.as_view()),
    path('new/', CreateSupplierView.as_view()),
    path('<uuid:pk>/', RetrieveSupplierView.as_view()),
    path('<uuid:pk>/', DestroySupplierView.as_view()),
]
