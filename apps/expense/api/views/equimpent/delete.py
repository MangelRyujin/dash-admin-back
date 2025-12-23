from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class EquipmentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)