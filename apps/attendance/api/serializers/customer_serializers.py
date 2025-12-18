from rest_framework import serializers
from apps.accounts.models import User

class AttendanceCustomerListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    has_attendance_today = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "type_document",
            "document",
            "has_attendance_today",
        ]
        
    def get_full_name(self, obj):
        return obj.get_full_name()