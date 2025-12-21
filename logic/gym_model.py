from geopy.distance import geodesic

"""Instance of a gym with relevant data"""

class Gym:
    def __init__(self, name, address, lat, lon, url=None):
        """intialize gym instance"""
        self.name = name
        self.address = address
        self.lat = lat
        self.lon = lon
        self.url = url

    def calculate_distance(self, origin_lat, origin_lon):
        """calculate distance from origin point to this gym"""
        self.distance_km = geodesic(
            (origin_lat, origin_lon),
            (self.lat, self.lon)
        ).km
        return self.distance_km



