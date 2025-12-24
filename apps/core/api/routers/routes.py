from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.core.api.views.equipment.create import EquipmentCreateAPIView
from apps.core.api.views.equipment.delete import EquipmentDeleteAPIView
from apps.core.api.views.equipment.list import EquipmentListAPIView
from apps.core.api.views.equipment.update import EquipmentUpdateAPIView
from apps.core.api.views.maintenance.create import EquipmentMaintenanceCreateAPIView
from apps.core.api.views.maintenance.delete import EquipmentMaintenanceDeleteAPIView
from apps.core.api.views.maintenance.list import EquipmentMaintenanceListAPIView
from apps.core.api.views.maintenance.update import EquipmentMaintenanceUpdateAPIView
from apps.core.api.views.plan_view import PlanViewSet
from apps.core.api.views.local_view import LocalViewSet
from apps.core.api.views.general_view import (
    LocalAndPlanListAPIView,
    LocalListAPIView,
    PlanListAPIView,
)

router = SimpleRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'locals', LocalViewSet, basename='local')

urlpatterns = [
    path('combo/all/', LocalAndPlanListAPIView.as_view(), name='combo-all'),
    path('combo/locals/', LocalListAPIView.as_view(), name='combo-locals'),
    path('combo/plans/', PlanListAPIView.as_view(), name='combo-plans'),
    
    # Equipment
    path("list/", EquipmentListAPIView.as_view(), name="equipment-list"),
    path("create/", EquipmentCreateAPIView.as_view(), name="equipment-create"),
    path("update/<int:pk>/", EquipmentUpdateAPIView.as_view(), name="equipment-update"),
    path("delete/<int:pk>/", EquipmentDeleteAPIView.as_view(), name="equipment-delete"),
    
    # Maintenance
    path("list/", EquipmentMaintenanceListAPIView.as_view(), name="equipment-maintenance-list"),
    path("create/", EquipmentMaintenanceCreateAPIView.as_view(), name="equipment-maintenance-create"),
    path("update/<int:pk>/", EquipmentMaintenanceUpdateAPIView.as_view(), name="equipment-maintenance-update"),
    path("delete/<int:pk>/", EquipmentMaintenanceDeleteAPIView.as_view(), name="equipment-maintenance-delete"),
]

urlpatterns += router.urls