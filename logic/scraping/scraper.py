"""scraper module to get gym data from web pages"""
import requests
from logic.gym_model import Gym

API_URL = "https://overpass.kumi.systems/api/interpreter" #overpass mirror

def fetch_gyms(lat, lon, radius=3000):
    """fetch gyms near lat/lon."""

    #setting up Overpass QL query
    query = f"""
    [out:json];
    (
      node["leisure"="fitness_centre"](around:{radius},{lat},{lon});
      way["leisure"="fitness_centre"](around:{radius},{lat},{lon});
    );
    out center;
    """


    response = requests.post(API_URL, data=query, timeout=20)
    response.raise_for_status() 
    data = response.json()

    #creating gyms list from the response data 
    gyms = []
    for el in data["elements"]:
        tags = el.get("tags", {})
        name = el["tags"].get("name", "Unknown Gym")
        address = el["tags"].get("addr:street", "Unknown address")

        #website url tags
        website = (
            tags.get("website")
            or tags.get("contact:website")
            or tags.get("url")
        )

        if "lat" in el:
            g_lat, g_lon = el["lat"], el["lon"]
        else:
            g_lat, g_lon = el["center"]["lat"], el["center"]["lon"]

        gyms.append(Gym(
    name=name,
    address=address,
    lat=g_lat,
    lon=g_lon,
    url=website
))

    return gyms