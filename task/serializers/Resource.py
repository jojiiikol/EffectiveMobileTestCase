from rest_framework import serializers

from task.models import Resource, User
from task.serializers.User import UserViewSerializer


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'owner')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    owner = UserViewSerializer(read_only=True)

class CreateResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'description')

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    def create(self, validated_data):
        resource = Resource(**validated_data)
        resource.owner = self.context['request'].user
        resource.save()
        return resource