from rest_framework import generics, permissions
from apps.attendance.api.serializers.attendance_serializers import AttendanceCreateSerializer
from apps.attendance.models import Attendance


class AttendanceCreateAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.select_related("user").all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            local_id_snapshot = self.request.user.local.pk if self.request.user.local else None,
            local_name_snapshot = self.request.user.local.name if self.request.user.local else None,
            registered_by=self.request.user
        )