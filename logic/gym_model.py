from geopy.distance import geodesic

"""Instance of a gym with relevant data"""

class Gym:
    def __init__(self, name, address, lat, lon, url=None, price_per_week=None):
        self.name = name
        self.address = address
        self.lat = lat
        self.lon = lon
        self.url = url
        self.price_per_week = price_per_week
        self.distance_km = None

    def calculate_distance(self, origin_lat, origin_lon):
        self.distance_km = geodesic(
            (origin_lat, origin_lon),
            (self.lat, self.lon)
        ).km
        return self.distance_km


