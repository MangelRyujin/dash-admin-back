from django.urls import path
from apps.expense.api.views.equipment.create import EquipmentCreateAPIView
from apps.expense.api.views.equipment.delete import EquipmentDeleteAPIView
from apps.expense.api.views.equipment.update import EquipmentUpdateAPIView
from apps.core.api.views.equipment_view import EquipmentListAPIView

urlpatterns = [
    path("list/", EquipmentListAPIView.as_view(), name="equipment-list"),
    path("create/", EquipmentCreateAPIView.as_view(), name="equipment-create"),
    path("update/<int:pk>/", EquipmentUpdateAPIView.as_view(), name="equipment-update"),
    path("delete/<int:pk>/", EquipmentDeleteAPIView.as_view(), name="equipment-delete")
]
