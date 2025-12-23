from rest_framework import serializers
from apps.core.models import Equipment, EquipmentMantenance

class EquipmentListSerializer(serializers.ModelSerializer):
    local_name = serializers.CharField(source='local.name', read_only=True)
    
    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "is_active",
            "local",
            "local_name",
            "created_at",
            "updated_at",
        ]
        

class EquipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "is_active",
            "local",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

      
class EquipmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "is_active",
            "local",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]