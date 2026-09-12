from django.contrib import admin
from apps.users.models import CustomUser, UserProfile

# Register your models here.


# rendu du model CustomUser dans django admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )


# rendu du model Profile dans django admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "created_at",
        "updated_at",
    )
