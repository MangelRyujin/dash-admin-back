from django.db import models

# Create your models here.

class Local(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locals"
        
    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=120)
    price = models.FloatField(default=0)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name="local_plans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        
    def __str__(self):
        return f"{self.name} - {self.local.name}"

class Equipment(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name="local_equipments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"
        
    def __str__(self):
        return f"{self.name} - {self.local.name}"
    
class EquipmentMantenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="equipment_maintenances")
    description = models.TextField()
    maintenance_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipment Maintenance"
        verbose_name_plural = "Equipment Maintenances"
        
    def __str__(self):
        return f"Maintenance for {self.equipment.name} on {self.maintenance_date.strftime('%Y-%m-%d')}"