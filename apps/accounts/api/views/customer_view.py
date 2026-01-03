
from apps.accounts.api.serializers.customer_serializer import CustomerRegisterSerializer, CustomerSerializer, CustomerUpdateSerializer, CustomerUpdateStatusSerializer
from apps.accounts.api.serializers.login_serializer import  User
from apps.accounts.api.serializers.user_serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.accounts.api.serializers.change_password_serializer import ChangePasswordSerializer
from utils.permission.admin import HasPermission

class CustomerRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = False
            user.is_verify = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "document",
        "email",
        "first_name",
        "last_name",
        "local__name",
    ]

    def get_queryset(self):
        user = self.request.user

        qs = User.objects.select_related("local").filter(
            is_staff=False,
        )

        if user.groups.filter(name="worker").exists():
            qs = qs.filter(local=user.local)

        return qs


class CustomerIdChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,HasPermission)
    
    def put(self, request, pk):
        user = get_object_or_404(User,pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password_1'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerToggleStatusAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, HasPermission)
    queryset = User.objects.all()
    serializer_class = CustomerUpdateStatusSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return Response(CustomerSerializer(user).data, status=status.HTTP_200_OK)

class CustomerUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,HasPermission)
    queryset = User.objects.all()
    serializer_class = CustomerUpdateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)