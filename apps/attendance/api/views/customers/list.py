from rest_framework import generics, permissions, filters
from apps.accounts.models import User
from apps.attendance.api.serializers.customer_serializers import AttendanceCustomerListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Exists, OuterRef
from apps.attendance.models import Attendance

class CustomerListByLocalAPIView(generics.ListAPIView):
    serializer_class = AttendanceCustomerListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = None
    filterset_fields = ["local"]
    search_fields = [
        'document',
        'first_name',  
        'last_name',  
    ]
    
    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()

        attendance_today = Attendance.objects.filter(
            user=OuterRef("pk"),
            created_at__date=today,
        )

        qs = User.objects.select_related("local").annotate(
            has_attendance_today=Exists(attendance_today)
        ).filter(
            is_active=True,
            is_staff=False,
            is_superuser=False
        )

        if user.groups.filter(name="worker").exists():
            qs = qs.filter(local=user.local)

        return qs.order_by("first_name", "last_name")