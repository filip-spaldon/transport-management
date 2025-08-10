from django.db import models
from django.utils.translation import gettext_lazy as _


class DriverAvailabilityStatusChoices(models.TextChoices):
    AVAILABLE = "AV", _("Available")
    ASSIGNED = "AS", _("Assigned")
