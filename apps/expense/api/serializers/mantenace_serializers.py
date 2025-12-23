from rest_framework import serializers
from apps.core.models import EquipmentMantenance

class EquipmentMantenanceListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EquipmentMantenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
        ]

class EquipmentMantenanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentMantenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        

class EquipmentMantenanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentMantenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]