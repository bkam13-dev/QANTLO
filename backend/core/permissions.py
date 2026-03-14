from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == "Admin" or request.user.role == "ADMIN")
    
class IsManager(BasePermission):

    def has_permission(self, request, view):
        return request.user and ((request.user.role in ["Manager", "Admin"]) or (request.user.role in ["MANAGER", "ADMIN"]))
    
    
class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user and ((request.user.role in ["Manager", "Admin", 'Staff']) or (request.user.role in ["MANAGER", "ADMIN", "STAFF"]))
