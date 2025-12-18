from django.urls import path

from apps.attendance.api.views.attendance.create import AttendanceCreateAPIView
from apps.attendance.api.views.attendance.delete import AttendanceDeleteTodayAPIView
from apps.attendance.api.views.customers.list import CustomerListByLocalAPIView


urlpatterns = [
    path(
        "customers/",
        CustomerListByLocalAPIView.as_view(),
        name="attendance-customer-list",
    ),
    path(
        "create/",
        AttendanceCreateAPIView.as_view(),
        name="attendance-create",
    ),
    path(
        "remove/today/",
        AttendanceDeleteTodayAPIView.as_view(),
        name="attendance-delete-today",
    ),
]