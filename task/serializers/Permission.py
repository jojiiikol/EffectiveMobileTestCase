from rest_framework import serializers

from task.models import Permission


class PermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('role', 'resource', 'read_access', 'update_access', 'delete_access', 'edit_permission_access')

