from decimal import Decimal as D

from django.db.models import DecimalField, ExpressionWrapper, F, Value
from django.db.models.functions import Power, Sqrt
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from driver.choices import DriverAvailabilityStatusChoices
from driver.models import Driver
from order.api.serializers import AssignmentSerializer, OrderSerializer, ShippingAddressSerializer
from order.choices import AssignmentStatusChoices, OrderStatusChoices
from order.models import Assignment, Order, ShippingAddress
from vehicle.choices import VehicleAvailabilityStatusChoices, VehicleTypeChoices
from vehicle.models import Vehicle


class ShippingAddressViewSet(ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=["post"])
    def assign_optimal_vehicle(self, request, pk=None):
        order = self.get_object()

        if Assignment.objects.filter(order=order).exists():
            return Response({"detail": _("Order already assigned.")}, status=status.HTTP_400_BAD_REQUEST)

        dest_lat = D(str(order.shipping_address.latitude))
        dest_lon = D(str(order.shipping_address.longitude))

        # Query vehicles and annotate with capacity difference, distance, and estimated cost
        vehicles_annotated = (
            Vehicle.objects.annotate(
                capacity_diff=F("max_capacity") - order.total_weight,
                lat_diff=F("current_position__latitude") - Value(dest_lat),
                lon_diff=F("current_position__longitude") - Value(dest_lon),
            )
            .annotate(
                distance=ExpressionWrapper(
                    Sqrt(Power(F("lat_diff"), 2) + Power(F("lon_diff"), 2)),
                    output_field=DecimalField(),
                ),
                estimated_cost=ExpressionWrapper(
                    F("cost_per_km") * Sqrt(Power(F("lat_diff"), 2) + Power(F("lon_diff"), 2)),
                    output_field=DecimalField(),
                ),
            )
            .filter(
                capacity_diff__gte=0,
                availability_status=VehicleAvailabilityStatusChoices.AVAILABLE,
            )
            .order_by("capacity_diff", "estimated_cost", "distance")
        )

        # Find the optimal vehicle (closest fit by capacity, cost, distance)
        vehicle = vehicles_annotated.first()
        if not vehicle:
            return Response({"detail": _("No suitable vehicle found.")}, status=status.HTTP_400_BAD_REQUEST)

        # Find any available driver
        driver = Driver.objects.filter(availability_status=DriverAvailabilityStatusChoices.AVAILABLE).first()
        if not driver:
            return Response({"detail": _("No available driver found.")}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare response data with clear reasoning for the assignment decision
        estimated_cost = vehicle.estimated_cost
        distance = vehicle.distance
        reasoning = (
            f"Selected {VehicleTypeChoices(vehicle.vehicle_type).label.lower()} {vehicle.licence_plate}: "
            f"capacity diff {vehicle.max_capacity - order.total_weight}, "
            f"estimated cost {round(estimated_cost, 2)}, "
            f"distance {round(distance, 2)}km, assigned driver {driver.name}."
        )

        # Mark vehicle and driver as assigned
        vehicle.assign()
        driver.assign()
        order.update_status(OrderStatusChoices.SHIPPED)

        # Create assignment record
        Assignment.objects.create(
            order=order,
            vehicle=vehicle,
            driver=driver,
            status=AssignmentStatusChoices.ASSIGNED,
        )

        # Return assignment info
        return Response(
            {
                "assigned_vehicle": vehicle.licence_plate,
                "assigned_driver": driver.name,
                "estimated_cost": round(estimated_cost, 2),
                "distance_km": round(distance, 2),
                "reasoning": reasoning,
            },
            status=status.HTTP_200_OK,
        )
