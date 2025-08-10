from rest_framework.serializers import ModelSerializer

from driver.api.serializers import DriverSerializer
from order.models import Assignment, Order, ShippingAddress
from vehicle.api.serializers import VehicleSerializer


class ShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ("id", "address", "city", "state", "zipcode", "latitude", "longitude")

    def create(self, validated_data):
        return ShippingAddress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class OrderSerializer(ModelSerializer):
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = ("id", "number", "customer_name", "status", "total_weight", "delivery_type", "shipping_address")

    def create(self, validated_data):
        shipping_address_data = validated_data.pop("shipping_address")
        shipping_address = ShippingAddressSerializer().create(shipping_address_data)
        order = Order.objects.create(shipping_address=shipping_address, **validated_data)
        return order

    def update(self, instance, validated_data):
        shipping_address_data = validated_data.pop("shipping_address", None)
        if shipping_address_data:
            ShippingAddressSerializer().update(instance.shipping_address, shipping_address_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AssignmentSerializer(ModelSerializer):
    order = OrderSerializer()
    vehicle = VehicleSerializer()
    driver = DriverSerializer()

    class Meta:
        model = Assignment
        fields = ("id", "order", "vehicle", "driver", "status", "assigned_at")

    def create(self, validated_data):
        order_data = validated_data.pop("order")
        vehicle_data = validated_data.pop("vehicle")
        driver_data = validated_data.pop("driver")
        order = OrderSerializer().create(order_data)
        vehicle = VehicleSerializer().create(vehicle_data)
        driver = DriverSerializer().create(driver_data)
        assignment = Assignment.objects.create(order=order, vehicle=vehicle, driver=driver, **validated_data)
        return assignment

    def update(self, instance, validated_data):
        order_data = validated_data.pop("order", None)
        vehicle_data = validated_data.pop("vehicle", None)
        driver_data = validated_data.pop("driver", None)
        if order_data:
            OrderSerializer().update(instance.order, order_data)
        if vehicle_data:
            VehicleSerializer().update(instance.vehicle, vehicle_data)
        if driver_data:
            DriverSerializer().update(instance.driver, driver_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
