import requests
from typing import List, Optional


def get_tourist_attractions(latitude: float, longitude: float, radius_km: int = 5, limit: int = 5) -> List[str]:
    """
    Fetch tourist attractions from Overpass API within a radius.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        radius_km: Radius in kilometers to search (default: 5)
        limit: Maximum number of attractions to return (default: 5)
        
    Returns:
        List of attraction names
    """
    # Overpass API query to find tourist attractions
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="attraction"](around:{radius_km * 1000},{latitude},{longitude});
      way["tourism"="attraction"](around:{radius_km * 1000},{latitude},{longitude});
    );
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(url, data=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        attractions = []
        seen_names = set()
        
        if "elements" in data:
            for element in data["elements"]:
                if "tags" in element and "name" in element["tags"]:
                    name = element["tags"]["name"]
                    if name and name not in seen_names:
                        attractions.append(name)
                        seen_names.add(name)
                        if len(attractions) >= limit:
                            break
        
        return attractions
    except Exception as e:
        print(f"Places service error: {e}")
        return []

