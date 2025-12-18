from django.db import models
from apps.accounts.models import User
from apps.core.models import Local

class Attendance(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    local_id_snapshot = models.IntegerField(null=True, blank=True)
    local_name_snapshot = models.CharField(max_length=200, blank=True, null=True)
    registered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendances_registered",
        verbose_name="register_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        ordering = ["-created_at"]

    def __str__(self):
        admin_name = self.registered_by.username if self.registered_by else "Sistema"
        return (
            f"Asistencia de {self.user} a las {self.created_at} "
            f"en {self.local_name_snapshot or 'Local desconocido'} "
            f"| Registrada por: {admin_name}"
        )
