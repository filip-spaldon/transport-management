from django.db import models
from django.utils.translation import gettext_lazy as _


class VehicleTypeChoices(models.TextChoices):
    VAN = "VA", _("Van")
    TRUCK = "TR", _("Truck")


class VehicleAvailabilityStatusChoices(models.TextChoices):
    AVAILABLE = "AV", _("Available")
    ASSIGNED = "AS", _("Assigned")
