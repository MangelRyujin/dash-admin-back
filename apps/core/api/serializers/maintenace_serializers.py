from rest_framework import serializers
from apps.core.models import EquipmentMaintenance
from apps.expense.models import Expense

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
    expense_amount = serializers.FloatField(write_only=True, required=False)
    expense_motive = serializers.CharField(write_only=True, required=False)
    expense_description = serializers.CharField(write_only=True, required=False)
    expense_date = serializers.DateTimeField(write_only=True, required=False)
    
    class Meta:
        model = EquipmentMaintenance
        fields = [
            "id",
            "equipment",
            "description",
            "maintenance_date",
            "created_at",
            "updated_at",
            # extra fields for expense creation
            "expense_amount",
            "expense_motive",
            "expense_description",
            "expense_date",
        ]
        read_only_fields = ["created_at", "updated_at"]
        
    def create(self, validated_data):
        expense_data = {
            "amount": validated_data.pop("expense_amount", None),
            "motive": validated_data.pop("expense_motive", None),
            "description": validated_data.pop("expense_description", None),
            "date_incurred": validated_data.pop("expense_date", None),
        }

        maintenance = EquipmentMaintenance.objects.create(**validated_data)

        if all(expense_data.values()): 
            Expense.objects.create(
                amount=expense_data["amount"],
                motive=expense_data["motive"],
                description=expense_data["description"],
                date_incurred=expense_data["date_incurred"],
                created_by=self.context["request"].user,
            )

        return maintenance
        

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