from rest_framework import serializers
from apps.core.models import EquipmentMaintenance

class EquipmentMaintenanceListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EquipmentMaintenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
        ]

class EquipmentMaintenanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentMaintenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        

class EquipmentMaintenanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentMaintenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]