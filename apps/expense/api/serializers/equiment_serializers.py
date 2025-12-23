from rest_framework import serializers
from apps.core.models import Equipment

class EquipmentListSerializer(serializers.ModelSerializer):    
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