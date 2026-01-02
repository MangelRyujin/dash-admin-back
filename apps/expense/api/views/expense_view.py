from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from apps.expense.models import Expense
from apps.expense.api.serializers.expense_serializer import ExpenseSerializer
from utils.permission.admin import IsAdminGroup

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, IsAdminGroup]
    serializer_class = ExpenseSerializer
    filter_backends = [ filters.SearchFilter]
    search_fields = ["motive"]  