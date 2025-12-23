from django.urls import path
from apps.expense.api.views.mantenance.create import EquipmentMantenanceCreateAPIView
from apps.expense.api.views.mantenance.delete import EquipmentMantenanceDeleteAPIView
from apps.expense.api.views.mantenance.update import EquipmentMantenanceUpdateAPIView
from apps.core.api.views.mantenance_view import EquipmentMantenanceListAPIView


urlpatterns = [
    path("list/", EquipmentMantenanceListAPIView.as_view(), name="equipment-mantenance-list"),
    path("create/", EquipmentMantenanceCreateAPIView.as_view(), name="equipment-mantenance-create"),
    path("update/<int:pk>/", EquipmentMantenanceUpdateAPIView.as_view(), name="equipment-mantenance-update"),
    path("delete/<int:pk>/", EquipmentMantenanceDeleteAPIView.as_view(), name="equipment-mantenance-delete"),
]