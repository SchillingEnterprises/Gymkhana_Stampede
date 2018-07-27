from rest_framework import mixins, viewsets, permissions

from .models import ChurchGoer
from .serializers import ChurchGoerSerializer


class ChurchGoerViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChurchGoer class"""

    queryset = ChurchGoer.objects.all()
    serializer_class = ChurchGoerSerializer
    permission_classes = [permissions.IsAuthenticated]


class CRUDViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = ChurchGoer.objects.all()
    serializer_class = ChurchGoerSerializer
    permission_classes = [permissions.IsAdminUser]
