from django.shortcuts import render
from apps.users.models import UserProfile,  CustomUser
from apps.users.serializers import CustomUserSerializer, UserProfileSerializer, DetailUserProfileSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

User = get_user_model()

class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return UserProfile.objects.select_related('user').filter(user=self.request.user)
    
    def get_serializer_class(self):
        if (self.action) == 'retrieve':
            return DetailUserProfileSerializer
        return UserProfileSerializer
        
    def get_object(self):
        return self.request.user.profile
    
    
class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)
    
    def get_object(self):
        return self.request.user
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.set_unusable_password()
        instance.save(
            update_fields = [
                "is_active",
                "password",
            ]
        )
