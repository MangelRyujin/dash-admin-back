from django.urls import path
from apps.expense.api.views.maintenance.create import EquipmentMaintenanceCreateAPIView
from apps.expense.api.views.maintenance.delete import EquipmentMaintenanceDeleteAPIView
from apps.expense.api.views.maintenance.update import EquipmentMaintenanceUpdateAPIView
from apps.core.api.views.maintenance_view import EquipmentMaintenanceListAPIView


urlpatterns = [
    path("list/", EquipmentMaintenanceListAPIView.as_view(), name="equipment-maintenance-list"),
    path("create/", EquipmentMaintenanceCreateAPIView.as_view(), name="equipment-maintenance-create"),
    path("update/<int:pk>/", EquipmentMaintenanceUpdateAPIView.as_view(), name="equipment-maintenance-update"),
    path("delete/<int:pk>/", EquipmentMaintenanceDeleteAPIView.as_view(), name="equipment-maintenance-delete"),
]