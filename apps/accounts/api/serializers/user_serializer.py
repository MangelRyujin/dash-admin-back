from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from apps.core.api.serializers.local_serializer import LocalSerializer
from apps.core.api.serializers.plan_serializer import PlanSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    
    local_detail = LocalSerializer(source="local", read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'province',
            'municipality',
            'address',
            'local',
            'local_detail',
            'is_active',
            'is_staff',
            'is_verify',
            'is_online',
            'type_document',
            'document',
            'last_login',
            'created_at',
            'updated_at',
            'groups'
        ]
        read_only_fields = [
            'id', 'email', 'last_login', 'created_at', 'updated_at', 'is_online', 'local_detail'
        ]
    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_online(self, obj):
        if obj.last_login:
            from django.utils import timezone
            return (timezone.now() - obj.last_login).total_seconds() < 900
        return False


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'local', 'plan')
    
    def validate_email(self,data):
        if data != None:
            return data
        else:
            raise ValidationError("email is required.")
     
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("La contraseña mínimo debe de tener 8 caracteres.")
        if data.lower() == data:
            raise ValidationError("La contraseña debe de tener al menos una mayúscula.")
        return data
    
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user