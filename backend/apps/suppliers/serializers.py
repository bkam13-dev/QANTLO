from rest_framework import serializers
from apps.suppliers.models import Supplier


class SupplierSerializers(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']