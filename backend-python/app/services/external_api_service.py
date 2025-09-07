"""
External API service for integrating with third-party services
"""
import httpx
from typing import Optional
from app.core.config import settings


class ExternalAPIService:
    """Service for external API integrations"""
    
    @staticmethod
    async def get_pixabay_image(query: str) -> Optional[str]:
        """
        Get image URL from Pixabay API
        """
        try:
            # Check if API key is placeholder or invalid
            if not settings.pixabay_api_key or settings.pixabay_api_key == "your_pixabay_api_key_here":
                print("Pixabay API key not configured, returning None")
                return None
                
            params = {
                "q": query,
                "key": settings.pixabay_api_key,
                "min_width": 1280,
                "min_height": 720,
                "image_type": "illustration",
                "category": "feelings"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://pixabay.com/api/",
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("hits"):
                    return data["hits"][0].get("largeImageURL")
                return None
                
        except Exception as e:
            print(f"Pixabay API Error: {e}")
            return None
    
    @staticmethod
    async def get_daily_prompt() -> str:
        """
        Get daily advice/prompt from AdviceSlip API
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.adviceslip.com/advice",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                return data.get("slip", {}).get("advice", "What's on your mind today?")
                
        except Exception as e:
            print(f"AdviceSlip API Error: {e}")
            return "What's on your mind today?"
