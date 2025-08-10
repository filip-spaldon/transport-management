from rest_framework import serializers

from vehicle.models import CurrentPosition, Vehicle


class CurrentPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentPosition
        fields = ("id", "latitude", "longitude")

    def create(self, validated_data):
        return CurrentPosition.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class VehicleSerializer(serializers.ModelSerializer):
    current_position = CurrentPositionSerializer()

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "licence_plate",
            "vehicle_type",
            "max_capacity",
            "cost_per_km",
            "availability_status",
            "current_position",
        )

    def create(self, validated_data):
        current_position_data = validated_data.pop("current_position")
        current_position = CurrentPositionSerializer().create(current_position_data)
        vehicle = Vehicle.objects.create(current_position=current_position, **validated_data)
        return vehicle

    def update(self, instance, validated_data):
        current_position_data = validated_data.pop("current_position", None)
        if current_position_data:
            CurrentPositionSerializer().update(instance.current_position, current_position_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
