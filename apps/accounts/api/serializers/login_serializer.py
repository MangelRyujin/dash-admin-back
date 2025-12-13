from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.accounts.api.serializers.user_serializer import GroupSerializer

User = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True)
    
    class Meta(UserDetailsSerializer.Meta):
        model = get_user_model()
        fields = UserDetailsSerializer.Meta.fields + (
            'first_name', 'last_name', 'full_name','type_document','document', 'phone_number', 'province', 
            'municipality', 'address', 'groups', 'local', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('email', 'created_at', 'last_login')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def validate_username(self, data):
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        
        token['email'] = user.email
        
        token['groups'] = list(user.groups.values_list('name', flat=True))
        
        if hasattr(user, 'document_type'):
            token['document_type'] = user.document_type
        if hasattr(user, 'document_id'):
            token['document_id'] = user.document_id
        if hasattr(user, 'phone_number'):
            token['phone_number'] = user.phone_number
        if hasattr(user, 'local'):
            token['local'] = user.local
            
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        user_serializer = CustomUserDetailsSerializer(self.user)
        
        data.update({
            'user': user_serializer.data
        })
        
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        
        try:
            access_token = AccessToken(attrs['access'])
            user_id = access_token['user_id']
            
            user = User.objects.get(id=user_id)

            user_serializer = CustomUserDetailsSerializer(user)
            data['user'] = user_serializer.data
            
        except (TokenError, User.DoesNotExist, KeyError):
            pass
            
        return data


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        
        try:
            access_token = AccessToken(attrs['token'])
            user_id = access_token['user_id']
            
            user = User.objects.get(id=user_id)
            
            user_serializer = CustomUserDetailsSerializer(user)
            data['user'] = user_serializer.data
            
        except (TokenError, User.DoesNotExist, KeyError):
            pass
            
        return data