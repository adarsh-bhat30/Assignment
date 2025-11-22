from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.request_models import ChatRequest
from models.response_models import ChatResponse
from services.geocoding import geocode_city
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent
import re

app = FastAPI()

# Add CORS middleware to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TourismAIOrchestrator:
    """Orchestrator class that coordinates between different agents."""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
    
    def extract_place_name(self, message: str) -> str:
        """
        Extract place name from user message using keywords 'to' or 'in'.
        
        Args:
            message: User's message text
            
        Returns:
            Extracted place name or empty string
        """
        # Look for patterns like "to <place>" or "in <place>"
        # Try case-insensitive search on original message to preserve capitalization
        patterns = [
            r'\bto\s+([A-Za-z\s]+?)(?:,|$)',
            r'\bin\s+([A-Za-z\s]+?)(?:,|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                place = match.group(1).strip()
                # Remove common trailing words that might have been captured
                place = re.sub(r'\s+(what|where|when|how|the|a|an)\s*$', '', place, flags=re.IGNORECASE)
                place = place.strip()
                if place:
                    return place
        
        return ""
    
    def detect_intent(self, message: str) -> dict:
        """
        Detect user intent from the message.
        
        Args:
            message: User's message text
            
        Returns:
            Dictionary with 'weather' and 'places' boolean flags
        """
        message_lower = message.lower()
        
        weather_keywords = ["weather", "temperature", "temp"]
        tourist_keywords = ["places", "visit", "attractions", "plan my trip"]
        
        weather_intent = any(keyword in message_lower for keyword in weather_keywords)
        places_intent = any(keyword in message_lower for keyword in tourist_keywords)
        
        return {
            "weather": weather_intent,
            "places": places_intent
        }
    
    def format_response(self, place_name: str, weather_data: dict = None, places_data: dict = None) -> str:
        """
        Format the response in natural language.
        
        Args:
            place_name: Name of the place
            weather_data: Dictionary with 'temperature' and 'precipitation_probability'
            places_data: Dictionary with 'attractions' list
            
        Returns:
            Formatted response string
        """
        weather_part = ""
        places_part = ""
        
        if weather_data:
            temp = int(weather_data["temperature"])
            rain_chance = int(weather_data["precipitation_probability"])
            weather_part = f"In {place_name} it's currently {temp}°C with a chance of {rain_chance}% to rain."
        
        if places_data and places_data.get("attractions"):
            attractions = places_data["attractions"]
            if attractions:
                places_list = "\n- ".join(attractions)
                places_part = f"In {place_name} these are the places you can go:\n- {places_list}"
            else:
                places_part = f"In {place_name} no tourist attractions were found nearby."
        
        # Combine responses
        if weather_part and places_part:
            # Extract just the attractions list part for the combined response
            if places_data and places_data.get("attractions") and places_data["attractions"]:
                attractions = places_data["attractions"]
                places_list = "\n- ".join(attractions)
                return f"{weather_part}\n\nAnd these are the places you can go:\n- {places_list}"
            else:
                return weather_part
        elif weather_part:
            return weather_part
        elif places_part:
            return places_part
        else:
            return f"Sorry, I couldn't fetch information for {place_name}."
    
    def process_request(self, message: str) -> str:
        """
        Process a user request and return a formatted response.
        
        Args:
            message: User's message text
            
        Returns:
            Formatted response string
        """
        # Extract place name
        place_name = self.extract_place_name(message)
        if not place_name:
            return "Sorry, I couldn't identify the place name in your message. Please mention a place using 'to' or 'in'."
        
        # Geocode the place
        coordinates = geocode_city(place_name)
        if not coordinates:
            return "Sorry, I don't know if this place exists."
        
        latitude, longitude = coordinates
        
        # Detect intent
        intent = self.detect_intent(message)
        
        weather_data = None
        places_data = None
        
        # Call appropriate agents
        if intent["weather"]:
            weather_data = self.weather_agent.process(place_name, latitude, longitude)
        
        if intent["places"]:
            places_data = self.places_agent.process(place_name, latitude, longitude)
        
        # If no intent detected, default to both
        if not intent["weather"] and not intent["places"]:
            weather_data = self.weather_agent.process(place_name, latitude, longitude)
            places_data = self.places_agent.process(place_name, latitude, longitude)
        
        # Format and return response
        return self.format_response(place_name, weather_data, places_data)


# Initialize orchestrator
orchestrator = TourismAIOrchestrator()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    POST endpoint to handle chat requests.
    
    Accepts: { "message": "<user text>" }
    Returns: { "reply": "<response text>" }
    """
    reply = orchestrator.process_request(request.message)
    return ChatResponse(reply=reply)


@app.get("/")
async def root():
    return {"message": "Tourism AI API is running"}

