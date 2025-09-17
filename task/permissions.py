from task.models import User, Resource
from task.models import Permission as ModelPermission
from rest_framework import permissions


def method_to_permission(request, permission: ModelPermission | None, view=None):
    if permission is None:
        return False
    if request.method == "GET":
        return permission.read_access
    if request.method == "PUT":
        return permission.update_access
    if request.method == "PATCH":
        return permission.update_access
    if request.method == "DELETE":
        return permission.delete_access
    if view.action == "set_permissions":
        return permission.edit_permission_access
    return False

class Permission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        permission = ModelPermission.objects.filter(role=request.user.role, resource=obj).first()
        return method_to_permission(request, permission, view)