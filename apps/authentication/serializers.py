
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


User = get_user_model()



class CustomLoginSerializer(LoginSerializer):
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = attrs.get('user')
        if user is None:
            raise serializers.ValidationError("Identifiants invalides.")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé.")
        return attrs
    
    
    
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['username'] = self.validated_data.get('username', "")
        data['email'] = self.validated_data.get('email', '')
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save(
            update_fields=[
                "first_name",
                "last_name",
            ]
        )
        return user
    
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    profile = serializers.SerializerMethodField()
    
    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "created_at",
            "updated_at",
        )
        
        read_only_fields = (
            "pk",
            "created_at",
            "updated_at",
        )
        
    def get_profile(self, obj):
        profile = obj.profile
    
        return {
            "avatar": (
                profile.avatar.url
                if profile.avatar
                else None
            ),
            "phone_number": profile.phone_number,
        }
    
    
    
    