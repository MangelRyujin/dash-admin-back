from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from apps.accounts.api.serializers.user_serializer import GroupSerializer
from apps.accounts.models import Membership, User
from apps.core.api.serializers.local_serializer import LocalSerializer
from apps.core.models import Plan
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import Membership
from apps.payments.models import Payment

class LastPaymentSerializer(serializers.ModelSerializer):
    payment_method_label = serializers.CharField(
        source="get_payment_method_display",
        read_only=True
    )

    registered_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "final_price",
            "discount_amount",
            "payment_method",
            "payment_method_label",

            "plan_id_snapshot",
            "plan_name_snapshot",
            "plan_price_snapshot",

            "local_name_snapshot",

            "paid_at",
            "paid_expires_at",

            "registered_by_name",
        ]

    def get_registered_by_name(self, obj):
        return obj.registered_by.get_full_name() if obj.registered_by else None

class MembershipSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = Membership
        fields = [
            "plan_id_snapshot",
            "plan_name_snapshot",
            "plan_price_snapshot",
            "started_at",
            "expires_at",
            "is_active",
            "is_expired",
        ]
        
class CustomerRegisterSerializer(serializers.ModelSerializer):
    plan_id = serializers.IntegerField(write_only=True)
    discount_amount = serializers.FloatField(required=False, default=0)
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'province',
            'local',
            'municipality',
            'address',
            'type_document',
            'document',
            "plan_id",
            "discount_amount",
        )
        
    def create(self, validated_data):
        plan_id = validated_data.pop("plan_id")
        discount_amount = validated_data.pop("discount_amount", 0)
        document = validated_data.get("document")
        payment_method=validated_data.get("payment_method", 0)
        validated_data["username"] = document
        validated_data["email"] = document + "@example.com"
        password = document
        user = User.objects.create_user(password=password,**validated_data)
        user.save()

        plan = Plan.objects.get(id=plan_id)

        paid_at = timezone.now()
        paid_expires_at = paid_at + timedelta(days=30)

        payment = Payment.objects.create(
            user=user,
            plan=plan,
            local=user.local,
            payment_method=payment_method,
            discount_amount=discount_amount,
            paid_expires_at=paid_expires_at,
            registered_by=self.context["request"].user,
            
        )

        membership, _ = Membership.objects.get_or_create(user=user)
        membership.apply_payment(payment)
        return user

class CustomerUpdateSerializer(serializers.ModelSerializer):

    local_detail = LocalSerializer(source="local", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    membership = MembershipSerializer(read_only=True)
    last_payment = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'province',
            'local',
            'municipality',
            'address',
            'type_document',
            'document',
            'is_active',
            'local_detail',
            'full_name',
            'is_online',
            'created_at',
            'membership',
            'last_payment',
        ]
        read_only_fields = [
            'id','last_login', 'created_at', 'updated_at', 'is_online', 'local_detail', 'membership', 'last_payment'
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    
    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_online(self, obj):
        if obj.last_login:
            from django.utils import timezone
            return (timezone.now() - obj.last_login).total_seconds() < 900
        return False
    
    def get_last_payment(self, obj):
        payment = (
            obj.payments
            .order_by("-paid_at")
            .first()
        )
        if not payment:
            return None
        return LastPaymentSerializer(payment).data
    
class CustomerUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active',
        ]


          
class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    membership = MembershipSerializer(read_only=True)
    local_detail = LocalSerializer(source="local", read_only=True)
    last_payment = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'province',
            'municipality',
            'address',
            'local',
            'local_detail',
            'is_active',
            'is_staff',
            'is_verify',
            'is_online',
            'type_document',
            'document',
            'last_login',
            'created_at',
            'updated_at',
            'membership',
            'last_payment',
        ]
        read_only_fields = [
            'id', 'email', 'last_login', 'created_at', 'updated_at', 'is_online', 'local_detail', 'membership', 'last_payment'
        ]
    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_online(self, obj):
        if obj.last_login:
            from django.utils import timezone
            return (timezone.now() - obj.last_login).total_seconds() < 900
        return False
    
    def get_last_payment(self, obj):
        payment = (
            obj.payments
            .order_by("-paid_at")
            .first()
        )
        if not payment:
            return None
        return LastPaymentSerializer(payment).data