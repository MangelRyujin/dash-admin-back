from django.urls import path
from rest_framework.routers import SimpleRouter

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
]

urlpatterns += router.urls