from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Only allow owners of an offer to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has the permission to edit or delete the offer.
        """
        if request.method in SAFE_METHODS:
            return True

        try:
            return obj.user == request.user
        except AttributeError:
            return getattr(obj.offer, 'user', None) == request.user

