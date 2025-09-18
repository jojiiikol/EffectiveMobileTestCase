from task.models import User, Resource, Role
from task.models import Permission as ModelPermission
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated


def get_user_role(request):
    role = request.user.role if request.user.is_authenticated else Role.objects.get(name="Guest")
    return role

def method_to_permission(request, permission: ModelPermission | None, view=None):
    if permission is None:
        return False
    if view.action == "set_permissions":
        return permission.edit_permission_access
    if request.method == "POST":
        return request.user.is_authenticated
    if request.method == "GET":
        return permission.read_access
    if request.method == "PUT":
        return permission.update_access
    if request.method == "PATCH":
        return permission.update_access
    if request.method == "DELETE":
        return permission.delete_access

    return False

class Permission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        user_role = get_user_role(request=request)
        permission = ModelPermission.objects.filter(role=user_role, resource=obj).first()
        return method_to_permission(request, permission, view)

class EditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_role = get_user_role(request=request)
        if obj.role == user_role and obj.edit_permission_access:
            return True
        if obj.resource.owner == request.user:
            return True
        return False



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user_role = get_user_role(request=request)
        if user_role == Role.objects.get(name="Admin"):
            return True
        return False

class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        resource = obj.resource
        if resource.owner == request.user:
            return True
        return False

def get_user_view_permissions(view):
    permission_classes = [AllowAny]
    if view.action == "list":
        permission_classes = [AllowAny]
    if view.action == "retrieve":
        permission_classes = [AllowAny]
    if view.action == "create":
        permission_classes = [AllowAny]
    if view.action == "update":
        permission_classes = [IsAdmin]
    if view.action == "delete":
        permission_classes = [IsAdmin]
    return [permission() for permission in permission_classes]

def get_permission_view_permissions(view):
    permission_classes = [AllowAny]
    if view.action == "list":
        permission_classes = [IsAdmin]
    if view.action == "update":
        permission_classes = [EditPermission | IsAdmin | IsOwnerPermission]
    if view.action == "delete":
        permission_classes = [EditPermission | IsAdmin | IsOwnerPermission]
    if view.action == "create":
        permission_classes = [IsAdmin]
    return [permission() for permission in permission_classes]

