from rest_framework import viewsets, permissions, filters
from apps.core.models import Local
from apps.core.api.serializers.local_serializer import LocalSerializer
from utils.permission.admin import IsAdminGroup

class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all().order_by('-created_at')
    serializer_class = LocalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminGroup]
    filter_backends = [ filters.SearchFilter]
    search_fields = ["name"]  
