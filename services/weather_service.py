import requests
from typing import Optional, Tuple


def get_weather(latitude: float, longitude: float) -> Optional[Tuple[float, float]]:
    """
    Fetch current weather data from Open-Meteo API.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        
    Returns:
        Tuple of (temperature, precipitation_probability) if successful, None otherwise
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": "precipitation_probability"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "current_weather" in data and "hourly" in data:
            temperature = data["current_weather"]["temperature"]
            # Get the first hour's precipitation probability
            precipitation_prob = 0
            if "precipitation_probability" in data["hourly"] and len(data["hourly"]["precipitation_probability"]) > 0:
                precipitation_prob = data["hourly"]["precipitation_probability"][0]
            return (temperature, precipitation_prob)
        return None
    except Exception as e:
        print(f"Weather service error: {e}")
        return None


