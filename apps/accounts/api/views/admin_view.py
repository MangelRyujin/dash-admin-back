from apps.accounts.api.serializers.admin_serializer import  AdminRegisterSerializer, AdminUpdateSerializer, AdminUpdateStatusSerializer
from apps.accounts.api.serializers.login_serializer import  User
from apps.accounts.api.serializers.user_serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.accounts.api.serializers.change_password_serializer import ChangePasswordSerializer
from utils.permission.admin import IsAdminGroup

class AdminRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminGroup]
    
    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = True
            user.is_verify = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminListView(generics.ListAPIView):
    
    queryset = User.objects.filter(is_staff = True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'document',
        'email',       
        'first_name',  
        'last_name',    
    ]


class AdminIdChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,IsAdminGroup)
    
    def put(self, request, pk):
        user = get_object_or_404(User,pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password_1'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminToggleStatusAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminGroup)
    queryset = User.objects.all()
    serializer_class = AdminUpdateStatusSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class AdminUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminGroup)
    queryset = User.objects.all()
    serializer_class = AdminUpdateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)