from rest_framework import serializers
from apps.core.models import Local


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]

