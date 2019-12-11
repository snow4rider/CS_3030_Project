from rest_framework import permissions


class IsRecipientOrSender(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Sender and Recipient can view message
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user.username or obj.recipient == request.user.username

        # Only recipient can modify message
        return obj.recipient == request.user.username
