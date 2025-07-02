from rest_framework import permissions

class IsReviewerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has the permission to edit or delete the review.
        """
        return request.method in permissions.SAFE_METHODS or obj.reviewer == request.user


class IsCustomerAndAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        Only authenticated users of type 'customer' are allowed.
        """
        return request.user.is_authenticated and request.user.type == 'customer'


         