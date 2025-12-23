from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from apps.core.models import Equipment
from apps.expense.api.serializers.equiment_serializers import EquipmentListSerializer
from utils.permission.admin import IsAdminGroup

class EquipmentListAPIView(generics.ListAPIView):
    queryset = Equipment.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentListSerializer
    filter_backends = [ filters.SearchFilter]
    search_fields = ["name"]  