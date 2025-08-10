from django.db import models

from core.models import CoreModel
from driver import choices as DriverChoices
from driver import querysets as DriverQuerySets


class Driver(CoreModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    licence_number = models.CharField(max_length=255)
    availability_status = models.CharField(max_length=2, choices=DriverChoices.DriverAvailabilityStatusChoices.choices)

    objects = DriverQuerySets.DriverQuerySet.as_manager()

    def assign(self):
        self.availability_status = DriverChoices.DriverAvailabilityStatusChoices.ASSIGNED
        self.save(update_fields=["availability_status"])
