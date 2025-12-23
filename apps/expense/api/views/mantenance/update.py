from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import EquipmentMantenance
from apps.expense.api.serializers.mantenace_serializers import EquipmentMantenanceUpdateSerializer
from utils.permission.admin import IsAdminGroup

class EquipmentMantenanceUpdateAPIView(generics.UpdateAPIView):
    queryset = EquipmentMantenance.objects.all()
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentMantenanceUpdateSerializer

    def perform_update(self, serializer):
        serializer.save()