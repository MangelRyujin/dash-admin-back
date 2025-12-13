from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.models import Local, Plan
from apps.core.api.serializers.general_serializer import GeneralLocalSerializer, GeneralPlanSerializer
from utils.permission.admin import IsAdminGroup



class LocalAndPlanListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get(self, request):
        locals_data = GeneralLocalSerializer(Local.objects.all(), many=True).data
        plans_data = GeneralPlanSerializer(Plan.objects.all(), many=True).data

        return Response({
            "locals": locals_data,
            "plans": plans_data
        })
        
class LocalListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locals_data = GeneralLocalSerializer(Local.objects.all(), many=True).data
        return Response(locals_data)
    
class PlanListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans_data = GeneralLocalSerializer(Plan.objects.all(), many=True).data
        return Response(plans_data)