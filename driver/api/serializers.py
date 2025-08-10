from rest_framework.serializers import ModelSerializer

from driver.models import Driver
from vehicle.api.serializers import VehicleSerializer


class DriverSerializer(ModelSerializer):

    class Meta:
        model = Driver
        fields = ("id", "name", "phone", "availability_status")

    def create(self, validated_data):
        return Driver.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
