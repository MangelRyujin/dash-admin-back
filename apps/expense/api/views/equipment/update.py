from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import Equipment
from apps.expense.api.serializers.equiment_serializers import EquipmentUpdateSerializer


class EquipmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Equipment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EquipmentUpdateSerializer

    def perform_update(self, serializer):
        serializer.save()