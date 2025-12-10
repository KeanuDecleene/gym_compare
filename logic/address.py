from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

class Address:
    def find_lat_lon(address: str):
        geolocator = Nominatim(user_agent="gym_compare")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        location = geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    

