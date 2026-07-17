from django.contrib import admin
from apps.users.models import CustomUser, UserProfile

# Register your models here.


# rendu du model CustomUser dans django admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

# rendu du model StockItem dans django admin


# rendu du model StockItem dans django admin
