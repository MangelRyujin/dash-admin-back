from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from apps.attendance.models import Attendance


class AttendanceDeleteTodayAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_id = request.data.get("user")
        today = timezone.now().date()
    
        if not user_id:
            return Response(
                {"detail": "El campo 'user' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        attendance = Attendance.objects.filter(
            user_id=user_id,
            created_at__date=today
        ).first()

        if not attendance:
            return Response(
                {"detail": "No existe asistencia para hoy."},
                status=status.HTTP_404_NOT_FOUND
            )

        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
