from django.urls import path, include
from apps.suppliers.views import CreateSupplierView, ListSupplierView, DestroySupplierView, RetrieveSupplierView

urlpatterns = [
    path('create/', CreateSupplierView.as_view()),
    path('<uuid:pk>/', RetrieveSupplierView.as_view()),
    path('<uuid:pk>/delete/', DestroySupplierView.as_view()),
    path('list/', ListSupplierView.as_view()),
]
