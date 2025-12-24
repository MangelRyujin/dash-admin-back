from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.expense.api.views.expense_view import ExpenseViewSet

router = SimpleRouter()
router.register('', ExpenseViewSet, basename='expense')

urlpatterns = []

urlpatterns += router.urls



