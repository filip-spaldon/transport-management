from django.db import models

from core.models import CoreModel
from vehicle import choices as VehicleChoices
from vehicle import querysets as VehicleQuerySets


class CurrentPosition(CoreModel):
    latitude = models.DecimalField(max_digits=10, decimal_places=2)
    longitude = models.DecimalField(max_digits=10, decimal_places=2)


class Vehicle(CoreModel):
    licence_plate = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=2, choices=VehicleChoices.VehicleTypeChoices.choices)
    max_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(
        max_length=2,
        choices=VehicleChoices.VehicleAvailabilityStatusChoices.choices,
    )
    current_position = models.ForeignKey(CurrentPosition, on_delete=models.PROTECT)

    objects = VehicleQuerySets.VehicleQuerySet.as_manager()

    def assign(self):
        self.availability_status = VehicleChoices.VehicleAvailabilityStatusChoices.ASSIGNED
        self.save(update_fields=["availability_status"])
