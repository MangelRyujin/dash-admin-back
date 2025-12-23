from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import EquipmentMaintenance
from utils.permission.admin import IsAdminGroup

class EquipmentMaintenanceDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminGroup]
    queryset = EquipmentMaintenance.objects.all()
    
    def perform_destroy(self, instance):
        instance.delete()
