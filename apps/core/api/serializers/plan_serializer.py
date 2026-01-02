from rest_framework import serializers
from apps.core.models import  Plan

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "price",
            "created_at",
            "updated_at",
        ]
