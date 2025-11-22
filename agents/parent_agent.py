from abc import ABC, abstractmethod


class ParentAgent(ABC):
    """Base class for all agents in the tourism system."""
    
    @abstractmethod
    def process(self, place_name: str, latitude: float, longitude: float) -> dict:
        """
        Process a request for a given place.
        
        Args:
            place_name: Name of the place
            latitude: Latitude of the place
            longitude: Longitude of the place
            
        Returns:
            Dictionary with processed data
        """
        pass

