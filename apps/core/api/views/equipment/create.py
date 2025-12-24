from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.core.models import Equipment
from apps.core.api.serializers.equiment_serializers import EquipmentCreateSerializer

class EquipmentCreateAPIView(generics.CreateAPIView):
    queryset = Equipment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EquipmentCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save()