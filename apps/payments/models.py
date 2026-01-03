from django.db import models
from django.core.validators import MinValueValidator
from apps.accounts.models import User
from apps.core.models import Plan, Local

class Payment(models.Model):
    PAYMENT_METHOD_TYPES = (
        (0, "CASH"),
        (1, "YAPE"),
        (2, "PLIN"),
        (3, "CARD"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)

    plan_id_snapshot = models.IntegerField(null=True, blank=True)
    plan_name_snapshot = models.CharField(max_length=200, blank=True, null=True)
    plan_price_snapshot = models.FloatField(default=0.0)

    local_id_snapshot = models.IntegerField(null=True, blank=True)
    local_name_snapshot = models.CharField(max_length=200, blank=True, null=True)

    payment_method = models.PositiveIntegerField(
        choices=PAYMENT_METHOD_TYPES,
        default=0
    )

    discount_amount = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.00)],
        blank=True,
        null=True
    )

    final_price = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.00)]
    )
    
    paid_at = models.DateTimeField(auto_now_add=True)

    paid_expires_at = models.DateTimeField()

    registered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments_registered",
        verbose_name="register_by"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-paid_at"]

    def save(self, *args, **kwargs):
        
        if self.plan and not self.plan_id_snapshot:
            self.plan_id_snapshot = self.plan.id
            self.plan_name_snapshot = self.plan.name
            self.plan_price_snapshot = self.plan.price

        if self.local and not self.local_id_snapshot:
            self.local_id_snapshot = self.local.id
            self.local_name_snapshot = self.local.name

        discount = self.discount_amount or 0
        self.final_price = max((self.plan_price_snapshot - discount), 0)

        super().save(*args, **kwargs)

    def __str__(self):
        admin_name = self.registered_by.username if self.registered_by else "Sistema"
        return (
            f"Pago de {self.user} por {self.plan_name_snapshot} "
            f"(Precio: ${self.plan_price_snapshot} | Desc: ${self.discount_amount or 0} | Final: ${self.final_price}) "
            f"en {self.local_name_snapshot or 'Local desconocido'} "
            f"| Registrado por: {admin_name} | Vence: {self.paid_expires_at.date()}"
        )
