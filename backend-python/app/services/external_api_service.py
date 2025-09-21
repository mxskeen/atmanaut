"""
External API service for integrating with third-party services
"""
import httpx
from typing import Optional
from app.core.config import settings


class ExternalAPIService:
    """Service for external API integrations"""

    # Pixabay integration removed

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
