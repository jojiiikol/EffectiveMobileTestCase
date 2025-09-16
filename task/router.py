from rest_framework import routers

from task.serializers.User import UserCreateSerializer
from task.views import UserViewSet, ResourceViewSet, PermissionViewSet

user_router = routers.SimpleRouter()
user_router.register(r'users', UserViewSet)

resource_router = routers.SimpleRouter()
resource_router.register(r'resource', ResourceViewSet)

permission_router = routers.SimpleRouter()
permission_router.register(r'permission', PermissionViewSet)
