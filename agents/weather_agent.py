from agents.parent_agent import ParentAgent
from services.weather_service import get_weather
from typing import Optional, Tuple


class WeatherAgent(ParentAgent):
    """Agent responsible for fetching weather information."""
    
    def process(self, place_name: str, latitude: float, longitude: float) -> dict:
        """
        Fetch weather data for a place.
        
        Returns:
            Dictionary with 'temperature' and 'precipitation_probability' keys,
            or None if weather data cannot be fetched
        """
        weather_data = get_weather(latitude, longitude)
        
        if weather_data:
            temperature, precipitation_prob = weather_data
            return {
                "temperature": temperature,
                "precipitation_probability": precipitation_prob
            }
        return None

