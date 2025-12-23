from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from apps.core.models import EquipmentMantenance
from apps.expense.api.serializers.equiment_serializers import EquipmentListSerializer
from utils.permission.admin import IsAdminGroup

class EquipmentMantenanceListAPIView(generics.ListAPIView):
    queryset = EquipmentMantenance.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = EquipmentListSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['equipment__name', 'description']
