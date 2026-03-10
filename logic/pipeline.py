from logic.address import Address
from logic.scraping.scraper import fetch_gyms
from logic.scraping.price_scraping import scrape_price_per_week

class GymPipeline:
    """fetching gyms and computing distances."""
    def __init__(self, limit=10):
        """initialize the gym pipeline with a limit on number of gyms."""
        self.limit = limit

    def run(self, address_str):
        origin_lat, origin_lon = Address.find_lat_lon(address_str)

        if origin_lat is None or origin_lon is None:
            return []

        gyms = fetch_gyms(origin_lat, origin_lon)

        for gym in gyms:
            gym.calculate_distance(origin_lat, origin_lon)

        gyms.sort(key=lambda g: g.distance_km)
        gyms = gyms[:self.limit]

        for gym in gyms:
            gym.price_per_week = scrape_price_per_week(gym.url)

        return gyms



        





