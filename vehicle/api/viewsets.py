from rest_framework.viewsets import ModelViewSet

from vehicle.api.serializers import VehicleSerializer
from vehicle.models import Vehicle


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer