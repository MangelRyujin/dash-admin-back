from rest_framework import viewsets, permissions, filters
from apps.core.models import Plan
from apps.core.api.serializers.plan_serializer import PlanSerializer
from utils.permission.admin import IsAdminGroup

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all().order_by('-created_at')
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminGroup]
    filter_backends = [ filters.SearchFilter]
    search_fields = ["name"]  

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()