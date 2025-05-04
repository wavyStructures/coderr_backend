from rest_framework import permissions

class IsReviewerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.reviewer == request.user

class IsCustomerAndAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'
    
         