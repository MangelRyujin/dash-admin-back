from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from apps.core.api.serializers.local_serializer import LocalSerializer

class CustomerRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'province',
            'local',
            'municipality',
            'address',
            'type_document',
            'document',
        )
        
    def create(self, validated_data):
        document = validated_data.get("document")
        validated_data["username"] = document
        validated_data["email"] = document + "@example.com"
        password = document
        user = User.objects.create_user(password=password,**validated_data)
        user.save()
        return user

class CustomerUpdateSerializer(serializers.ModelSerializer):

    local_detail = LocalSerializer(source="local", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'province',
            'local',
            'municipality',
            'address',
            'type_document',
            'document',
            'is_active',
            'local_detail',
            'full_name',
            'is_online'
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    
    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_online(self, obj):
        if obj.last_login:
            from django.utils import timezone
            return (timezone.now() - obj.last_login).total_seconds() < 900
        return False
    
class CustomerUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active',
        ]