from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from apps.core.api.serializers.local_serializer import LocalSerializer

class AdminGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")
        read_only_fields = ("id",)

   
class AdminRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'province',
            'local',
            'municipality',
            'address',
            'type_document',
            'document',
            'groups',
        )
        
    def validate_email(self, data):
        if not data:
            raise ValidationError("El email es obligatorio.")
        return data
    
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("The password must have more than 8 characters.")
        if data.lower() == data:
            raise ValidationError("The password must have at least one capital letter.")
        return data
    
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        email = validated_data.get("email")
        validated_data["username"] = email
        user = User.objects.create_user(**validated_data)
        if groups_data:
            group_ids = [group.id for group in groups_data]
            groups = Group.objects.filter(id__in=group_ids)
            user.groups.set(groups)
        user.save()
    
        return user

class AdminUpdateSerializer(serializers.ModelSerializer):
    groups = AdminGroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), write_only=True, source='groups'
    )
    local_detail = LocalSerializer(source="local", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
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
            'groups',
            'group_ids',
            'local_detail',
            'full_name',
            'is_online'
        ]

    def update(self, instance, validated_data):
        groups = validated_data.pop('group_ids', None)
        instance = super().update(instance, validated_data)
        if groups is not None:
            instance.groups.set(groups)
        return instance
    
    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_online(self, obj):
        if obj.last_login:
            from django.utils import timezone
            return (timezone.now() - obj.last_login).total_seconds() < 900
        return False
    
class AdminUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active',
        ]