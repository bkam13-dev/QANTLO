from rest_framework import serializers
from apps.users.models import CustomUser, UserProfile


# Serializer du model Utilisateur Personnalisé
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'first_name', 'last_name', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'email', 'role', 'created_at', 'updated_at']
        
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attrs, value in validated_data.items:
            setattr(instance, attrs, value)
        instance.save()
        if profile_data is not None:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            for attrs, value in profile_data.items:
                setattr(profile, attrs, value)
            profile.save()
        return instance

# Serializer du model Profil Utilisateur    
class UserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'avatar']
        # read_only_fields = ['user']
        
    def validate_phone(self, value):
        if value is None:
            return value
        
        if not value:
            return value
        
        value = value.strip()
        
        if value and len(value) < 10 or len(value()) > 20:
            raise serializers.ValidationError("Veuillez entrer un numéro de téléphone valide")
        return value


class DetailUserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'avatar']
        read_only_fields = ['user', 'phone_number', 'avatar']