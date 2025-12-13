from apps.accounts.api.serializers.login_serializer import CustomTokenObtainPairSerializer, User
from apps.accounts.api.serializers.user_serializer import UserRegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny



class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token_serializer = CustomTokenObtainPairSerializer()
            refresh = token_serializer.get_token(user)
            access = refresh.access_token

            user_data = UserSerializer(user).data

            return Response({
                "refresh": str(refresh),
                "access": str(access),
                "user": user_data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


