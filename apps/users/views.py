from django.shortcuts import render
from apps.users.models import CustomUser, UserProfile
from apps.users.serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework import viewsets

# Create your views here.



class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer