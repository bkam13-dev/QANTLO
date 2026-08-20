from rest_framework import serializers
from apps.users.models import CustomUser, UserProfile



# Serializer du model Utilisateur Personnalisé
class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = CustomUser
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']
        read_only_fields = ['id']
        
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les passwords ne correspondent pas."})
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

# Serializer du model Profil Utilisateur    
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'phone']
        read_only_fields = ['user']


class DetailUserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'phone']
        read_only_fields = ['user']