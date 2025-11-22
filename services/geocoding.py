import requests
from typing import Optional, Tuple


def geocode_city(city_name: str) -> Optional[Tuple[float, float]]:
    """
    Geocode a city name to latitude and longitude using Nominatim API.
    
    Args:
        city_name: Name of the city to geocode
        
    Returns:
        Tuple of (latitude, longitude) if found, None otherwise
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "TourismAI/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return (lat, lon)
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None


