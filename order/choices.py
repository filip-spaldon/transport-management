from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderDeliveryTypeChoices(models.TextChoices):
    DELIVERY = "DE", _("Delivery")
    PICKUP = "PI", _("Pickup")


class OrderStatusChoices(models.TextChoices):
    CREATED = "CR", _("Created")
    SHIPPED = "SH", _("Shipped")
    DELIVERED = "DL", _("Delivered")
    CANCELLED = "CL", _("Cancelled")


class AssignmentStatusChoices(models.TextChoices):
    ASSIGNED = "AS", _("Assigned")
    COMPLETED = "CL", _("Completed")
