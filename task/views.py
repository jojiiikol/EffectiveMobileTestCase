from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Trunc
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from task.models import User, Resource, Permission
from task.serializers.Permission import PermissionCreateSerializer
from task.serializers.Resource import ResourceSerializer, CreateResourceSerializer
from task.serializers.User import UserViewSerializer, UserCreateSerializer, UserUpdateSerializer



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
        user = self.request.user
        user = UserViewSerializer(user)
        return Response(user.data)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateResourceSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=['POST'], detail=True)
    def set_permissions(self):
        pass

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = PermissionCreateSerializer
        return super().create(request, *args, **kwargs)


