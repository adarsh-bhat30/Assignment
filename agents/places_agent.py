from agents.parent_agent import ParentAgent
from services.places_service import get_tourist_attractions


class PlacesAgent(ParentAgent):
    """Agent responsible for fetching tourist attractions."""
    
    def process(self, place_name: str, latitude: float, longitude: float) -> dict:
        """
        Fetch tourist attractions for a place.
        
        Returns:
            Dictionary with 'attractions' key containing list of attraction names
        """
        attractions = get_tourist_attractions(latitude, longitude, radius_km=5, limit=5)
        
        return {
            "attractions": attractions
        }

