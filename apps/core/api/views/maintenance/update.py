from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import EquipmentMaintenance
from apps.core.api.serializers.maintenace_serializers import EquipmentMaintenanceUpdateSerializer
from utils.permission.admin import IsAdminGroup

class EquipmentMaintenanceUpdateAPIView(generics.UpdateAPIView):
    queryset = EquipmentMaintenance.objects.all()
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentMaintenanceUpdateSerializer

    def perform_update(self, serializer):
        serializer.save()