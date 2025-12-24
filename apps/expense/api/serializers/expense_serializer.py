from rest_framework import serializers
from apps.expense.models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "motive",
            "description",
            "date_incurred",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]
