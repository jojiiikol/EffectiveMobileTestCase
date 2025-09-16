from asyncio import Task

from django.contrib import admin

from task.models import Role, User, Resource


# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass