from django.urls import path, include
from apps.accounts.views import GoogleLoginView
from django.contrib.auth import views

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    

]
