from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    
    def has_permission(self, request, view):

        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name='admin').exists()
        )
        
class HasPermission(BasePermission):
    
    def has_permission(self, request, view):

        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name__in=["admin", "worker"]).exists()
        )