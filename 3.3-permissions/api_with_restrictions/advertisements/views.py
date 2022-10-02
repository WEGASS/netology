from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrAdmin, IsNotOwner


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    def get_queryset(self):
        user = self.request.user.id
        queryset = Advertisement.objects.exclude(Q(status='DRAFT') & ~Q(creator=user))
        return queryset

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'add_to_favorites':
            return [IsAuthenticated(), IsNotOwner()]
        elif self.action == 'remove_from_favorites':
            return [IsAuthenticated()]
        elif self.action == 'favorites':
            return [IsAuthenticated()]
        return []

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        user = request.user
        adv = get_object_or_404(self.get_queryset(), pk=pk)
        if adv in user.favorites.all():
            return Response({'status': 'Adv already in favorites'})
        elif adv.creator == user:
            return Response({'status': 'Can not be done. Adv created by user'})
        user.favorites.add(adv)
        return Response({'status': 'Adv added to favorites'})

    @action(detail=True, methods=['delete'])
    def remove_from_favorites(self, request, pk=None):
        user = request.user
        adv = get_object_or_404(self.get_queryset(), pk=pk)
        if adv in user.favorites.all():
            user.favorites.remove(adv)
            return Response({'status': 'Adv was removed from favorites'})
        return Response({'status': 'Adv is not in favorites'})

    @action(detail=False, permission_classes=[IsAuthenticated])
    def favorites(self, request):
        user_favorites = Advertisement.objects.filter(in_favorites=request.user)
        serializer = self.get_serializer(user_favorites, many=True)
        return Response(serializer.data)