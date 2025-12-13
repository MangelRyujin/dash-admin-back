from rest_framework import serializers
from apps.core.api.serializers.local_serializer import LocalSerializer
from apps.core.models import Local, Plan

class PlanSerializer(serializers.ModelSerializer):
    local_detail = LocalSerializer(read_only=True)
    local = serializers.PrimaryKeyRelatedField(queryset=Local.objects.all())

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "price",
            "local",
            "local_detail",
            "created_at",
            "updated_at",
        ]
