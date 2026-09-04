from django.shortcuts import render
from apps.users.models import CustomUser, UserProfile
from apps.users.serializers import CustomUserSerializer, UserProfileSerializer, DetailUserProfileSerializer
from rest_framework import viewsets

# Create your views here.



class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    
    def get_serializer_class(self):
        if (self.action) not in ['list', 'retrieve']:
            return UserProfileSerializer
        return DetailUserProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)