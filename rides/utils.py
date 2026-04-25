from decimal import Decimal
from math import asin, cos, radians, sin, sqrt


def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return earth_radius_km * c


def calculate_price(distance_km):
    base_fare = Decimal('100')
    per_km_rate = Decimal('20')
    distance_decimal = Decimal(str(distance_km))
    total_price = base_fare + (per_km_rate * distance_decimal)
    return total_price.quantize(Decimal('0.01'))
