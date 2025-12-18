from django.utils import timezone
from rest_framework import serializers
from apps.attendance.models import Attendance

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "user",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        user = attrs.get("user")
        today = timezone.now().date()

        if Attendance.objects.filter(
            user=user,
            created_at__date=today
        ).exists():
            raise serializers.ValidationError(
                "Este usuario ya tiene una asistencia registrada hoy."
            )

        return attrs