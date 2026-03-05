from django.urls import path, include


urlpatterns = [
    path('allauth/', include('allauth.urls')),

]
