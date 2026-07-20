from rest_framework import serializers
from apps.users.models import CustomUser, UserProfile



# Serializer du model Utilisateur Personnalisé
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']
        read_only_fields = ['id']
        
        

# Serializer du model Profil Utilisateur    
class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'phone']
        read_only_fields = []
