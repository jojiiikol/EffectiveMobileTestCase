from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=False, blank=False, default=1, related_name='users')

    def __str__(self):
        return self.username

class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions_role')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions_resource')
    read_access = models.BooleanField(default=False)
    update_access = models.BooleanField(default=False)
    delete_access = models.BooleanField(default=False)
    edit_permission_access = models.BooleanField(default=False)