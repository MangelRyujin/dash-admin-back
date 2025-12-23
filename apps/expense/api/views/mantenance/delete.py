from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import EquipmentMantenance
from utils.permission.admin import IsAdminGroup

class EquipmentMantenanceDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminGroup]
    queryset = EquipmentMantenance.objects.all()
    
    def perform_destroy(self, instance):
        instance.delete()
