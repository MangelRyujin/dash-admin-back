from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.core.models import Equipment

class EquipmentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Equipment.objects.all()
    
    def perform_destroy(self, instance):
        instance.delete()
            
        