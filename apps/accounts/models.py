from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from apps.core.models import Local, Plan
from utils.validates.general import validate_phone_number

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)

        if User.objects.filter(username=username).exists():
            raise ValueError("Ya existe un usuario con este nombre de usuario")

        if User.objects.filter(email=email).exists():
            raise ValueError("Ya existe un usuario con este email")

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.is_verify = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        Authentication by case-insensitive.
        """
        return self.get(username__iexact=username)

class User(AbstractUser):
    DOCUMENT_TYPES = (
        ("DNI", "DNI"),
        ("CE", "Carné de Extranjería"),
        ("PAS", "Pasaporte"),
    )
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        validators=[validate_phone_number],
        verbose_name="Teléfono"
    )
    email = models.EmailField(unique=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    type_document = models.CharField(
        max_length=3,
        choices=DOCUMENT_TYPES,
        default="DNI",
        verbose_name="document_type"
    )
    document = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_verify = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    REQUIRED_FIELDS=["email"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_username()}"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_short_name(self):
        return self.first_name if self.first_name else self.email.split('@')[0]

    @property
    def is_admin(self):
        return self.groups.filter(name='admin').exists() or self.is_staff
    
class Membership(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="membership"
    )
    
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name="memberships")
    plan_id_snapshot = models.IntegerField(null=True, blank=True)
    plan_name_snapshot = models.CharField(max_length=200, blank=True, null=True)
    plan_price_snapshot = models.FloatField(default=0)
    plan_duration_days_snapshot = models.IntegerField(default=0)
    
    local_id_snapshot = models.IntegerField(null=True, blank=True)
    local_name_snapshot = models.CharField(max_length=200, null=True, blank=True)
    
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def apply_payment(self, payment):

        if self.plan_id_snapshot:
            try:
                self.plan = Plan.objects.get(id=self.plan_id_snapshot)
            except Plan.DoesNotExist:
                self.plan = None

        self.plan_id_snapshot = payment.plan_id_snapshot
        self.plan_name_snapshot = payment.plan_name_snapshot
        self.plan_price_snapshot = payment.plan_price_snapshot
        
        self.plan_duration_days_snapshot = (
            (payment.paid_expires_at - payment.paid_at).days
        )

        self.local_id_snapshot = payment.local_id_snapshot
        self.local_name_snapshot = payment.local_name_snapshot

        self.started_at = payment.paid_at
        self.expires_at = payment.paid_expires_at
        self.is_active = True

        self.save()

    def __str__(self):
        return f"Membresía de {self.user} (vence {self.expires_at})"
    
    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()