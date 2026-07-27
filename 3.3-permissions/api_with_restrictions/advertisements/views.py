from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Advertisement
from .serializers import AdvertisementSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешение: только автор или админ может редактировать/удалять."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_staff


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'created_at']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()