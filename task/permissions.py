from task.models import User, Resource
from task.models import Permission as ModelPermission
from rest_framework import permissions


def method_to_permission(request, permission: ModelPermission | None):
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

class Permission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        permission = Permission.objects.get(role=request.user.role, resource=obj.resource)
        return method_to_permission(request, permission)