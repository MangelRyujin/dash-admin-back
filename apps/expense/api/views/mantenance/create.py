from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import EquipmentMantenance
from utils.permission.admin import IsAdminGroup
from apps.expense.api.serializers.mantenace_serializers import EquipmentMantenanceCreateSerializer


class EquipmentMantenanceCreateAPIView(generics.CreateAPIView):
    queryset = EquipmentMantenance.objects.all()
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentMantenanceCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save()