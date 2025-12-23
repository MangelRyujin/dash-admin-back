from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import EquipmentMaintenance
from utils.permission.admin import IsAdminGroup
from apps.expense.api.serializers.maintenace_serializers import EquipmentMaintenanceCreateSerializer


class EquipmentMaintenanceCreateAPIView(generics.CreateAPIView):
    queryset = EquipmentMaintenance.objects.all()
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentMaintenanceCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save()