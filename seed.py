# Seed script for demo data
import random

from driver.choices import DriverAvailabilityStatusChoices
from driver.models import Driver
from order.choices import OrderDeliveryTypeChoices, OrderStatusChoices
from order.models import Order, ShippingAddress
from vehicle.choices import VehicleAvailabilityStatusChoices, VehicleTypeChoices
from vehicle.models import CurrentPosition, Vehicle

# Helper to create random coordinates
CITY_CENTER = (48.15, 17.11)  # Example: Bratislava


def random_coord(center, spread=0.1):
    return round(center[0] + random.uniform(-spread, spread), 5), round(center[1] + random.uniform(-spread, spread), 5)


def run():
    # Vehicles
    num_vehicles = random.randint(5, 10)
    vehicles = []
    for i in range(num_vehicles):
        lat, lon = random_coord(CITY_CENTER)
        pos = CurrentPosition.objects.create(latitude=lat, longitude=lon)
        v = Vehicle.objects.create(
            licence_plate=f"ABC-{100 + i}",
            vehicle_type=VehicleTypeChoices.TRUCK if i % 2 == 0 else VehicleTypeChoices.VAN,
            max_capacity=random.randint(1000, 5000),
            cost_per_km=round(random.uniform(1.2, 2.5), 2),
            availability_status=VehicleAvailabilityStatusChoices.AVAILABLE,
            current_position=pos,
        )
        vehicles.append(v)

    # Drivers
    num_drivers = random.randint(3, 5)
    drivers = []
    for i in range(num_drivers):
        d = Driver.objects.create(
            name=f"Driver {i + 1}",
            phone=f"+4219000000{i}",
            licence_number=f"DRV{i + 1:03}",
            availability_status=DriverAvailabilityStatusChoices.AVAILABLE,
        )
        drivers.append(d)

    # Shipping addresses
    addresses = []
    for i in range(3):
        lat, lon = random_coord(CITY_CENTER, spread=0.2)
        addr = ShippingAddress.objects.create(
            address=f"Sample Street {i + 1}",
            city="Bratislava",
            state="BA",
            zipcode=f"8110{i}",
            latitude=lat,
            longitude=lon,
        )
        addresses.append(addr)

    # Orders
    num_orders = random.randint(2, 3)
    for i in range(num_orders):
        Order.objects.create(
            number=f"ORD-{i + 1:03}",
            customer_name=f"Customer {i + 1}",
            status=OrderStatusChoices.CREATED,
            total_weight=random.randint(1200, 3500),
            delivery_type=OrderDeliveryTypeChoices.DELIVERY,
            shipping_address=addresses[i % len(addresses)],
        )
    print("Seed data created.")
