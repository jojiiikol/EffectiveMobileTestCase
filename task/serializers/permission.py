from rest_framework import serializers

from task.models import Permission, Role
from task.serializers.resource import ResourceSerializer
from task.serializers.role import RoleSerializer


class PermissionResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'role', 'resource', 'read_access', 'update_access', 'delete_access', 'edit_permission_access')

    role = RoleSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)


class PermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('role_id', 'resource_id', 'read_access', 'update_access', 'delete_access', 'edit_permission_access')

    role_id = serializers.IntegerField(required=True)
    resource_id = serializers.IntegerField(read_only=True)
    read_access = serializers.BooleanField(required=True)
    update_access = serializers.BooleanField(required=True)
    delete_access = serializers.BooleanField(required=True)
    edit_permission_access = serializers.BooleanField(required=True)

    def validate(self, attrs):
        if not Role.objects.filter(id=attrs['role_id']).exists():
            raise serializers.ValidationError('Role does not exist')
        if Permission.objects.filter(role_id=attrs['role_id'], resource_id=self.context["object"].id).exists():
            raise serializers.ValidationError('Permission already exists, please update them')

    def create(self, validated_data):
        permission = Permission(**validated_data, resource=self.context["object"])
        permission.save()
        return permission


