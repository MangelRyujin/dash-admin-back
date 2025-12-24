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
        
    # aqui en el create debes de hacer algo  para por ejemplo que recibir un dato extra por la 
    # request para crear un gasto asociado a un mantenimiento
    # ejemplo de lo qe recibes extra:
    
    # expense_amount = serializers.FloatField(write_only=True, required=False)
    # expense_motive = serializers.CharField(write_only=True, required=False)
    # expense_description = serializers.CharField(write_only=True, required=False)
    # expense_date = serializers.DateTimeField(write_only=True, required=False)
    
    # modificas el create
    
    # def create(self,validated_data):
    #     pass
        

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