from django.db import models

from core.models import CoreModel
from driver.models import Driver
from order import choices as OrderChoices
from order import querysets as OrderQuerySets
from vehicle.models import Vehicle


class ShippingAddress(CoreModel):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

    latitude = models.DecimalField(max_digits=10, decimal_places=2)
    longitude = models.DecimalField(max_digits=10, decimal_places=2)

    objects = OrderQuerySets.ShippingAddressQuerySet.as_manager()


class Order(CoreModel):
    number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=OrderChoices.OrderStatusChoices.choices)
    total_weight = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_type = models.CharField(max_length=2, choices=OrderChoices.OrderDeliveryTypeChoices.choices)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT)

    objects = OrderQuerySets.OrderQuerySet.as_manager()

    def update_status(self, status):
        self.status = status
        self.save(update_fields=["status"])


class Assignment(CoreModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=OrderChoices.AssignmentStatusChoices.choices)

    objects = OrderQuerySets.AssignmentQuerySet.as_manager()
