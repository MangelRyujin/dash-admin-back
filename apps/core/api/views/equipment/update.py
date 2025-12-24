from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import Equipment
from apps.core.api.serializers.equiment_serializers import EquipmentUpdateSerializer
from utils.permission.admin import IsAdminGroup

class EquipmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Equipment.objects.all()
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentUpdateSerializer

    def perform_update(self, serializer):
        serializer.save()