from rest_framework import permissions


class IsUserOrModifying(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return True

        return obj.username == request.user.username