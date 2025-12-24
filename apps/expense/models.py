from django.db import models
from django.core.validators import MinValueValidator
from apps.accounts.models import User
# Create your models here.

class Expense(models.Model):
    EXPENSE_TYPES = (
        (0, "expense"),
        (1, "income"),
    )
    motive = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    type_document = models.IntegerField(
        choices=EXPENSE_TYPES,
        default=0,
        verbose_name="expense_type"
    )
    amount = models.FloatField(default=0 , validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="expenses_created_by", blank=True, null=True)
    date_incurred = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        
    def __str__(self):
        return f"{self.description} - ${self.amount} on {self.date_incurred.strftime('%Y-%m-%d')}"
    
class PaymentWorker(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="worker_payments", blank=True, null=True)
    worker_id = models.CharField(max_length=20)
    worker_name = models.CharField(max_length=120)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, related_name="worker_payments", blank=True, null=True)
    amount = models.FloatField(default=0 , validators=[MinValueValidator(0)])
    payment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="payment_expenses_created_by", blank=True, null=True)
    
    class Meta:
        verbose_name = "Payment Worker"
        verbose_name_plural = "Payment Workers"
        
    def __str__(self):
        return f"Payment to {self.worker_name} - ${self.amount} on {self.payment_date.strftime('%Y-%m-%d')}"