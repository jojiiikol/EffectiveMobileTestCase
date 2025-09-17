from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Trunc
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from task.models import User, Resource, Permission
from task.serializers.permission import PermissionCreateSerializer, PermissionResourceSerializer
from task.serializers.resource import ResourceSerializer, CreateResourceSerializer
from task.serializers.User import UserViewSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserInfoUpdateSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(request=UserCreateSerializer, responses=UserViewSerializer)
    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def me(self, request, *args, **kwargs):
        user = request.user
        user = self.serializer_class(user).data
        return Response(user)

    @me.mapping.put
    def me_update(self, request, *args, **kwargs):
        user = request.user
        new_data = UserUpdateSerializer(user, data=request.data)
        if new_data.is_valid():
            new_data.save()
            return Response(new_data.data)
        return Response(new_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @me.mapping.delete
    def me_delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user.is_active = False
            user.save()
            return Response({"data": "Your account has been deactivated."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateResourceSerializer
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(request=PermissionCreateSerializer)
    @action(methods=['POST'], detail=True)
    def set_permissions(self, request, *args, **kwargs):
        permissions = PermissionCreateSerializer(data=request.data, context={'object': self.get_object()})
        if permissions.is_valid():
            permissions.save()
            return Response(permissions.data)
        return Response(permissions.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = PermissionCreateSerializer
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = PermissionResourceSerializer
        return super().list(request, *args, **kwargs)


