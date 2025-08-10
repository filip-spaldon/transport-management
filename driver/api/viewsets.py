from rest_framework import viewsets

from driver.api.serializers import DriverSerializer
from driver.models import Driver


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
