from rest_framework import serializers
from apps.core.models import Local,Plan


class GeneralLocalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Local
        fields = [
            "id",
            "name",
        ]

class GeneralPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
        ]

