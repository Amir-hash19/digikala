from rest_framework.permissions import BasePermission



class IsSupportUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == "Support" and request.user.groups.filter(name="support")
        





class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == "Admin" and request.user.groups.filter(name="Admin")


