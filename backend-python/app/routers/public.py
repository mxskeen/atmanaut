from fastapi import APIRouter, Request
from app.middleware import limiter
from app.services.external_api_service import ExternalAPIService

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/daily-prompt")
@limiter.limit("100/hour")
async def get_daily_prompt(request: Request):
    """
    Get daily writing prompt from AdviceSlip API
    """
    try:
        prompt = await ExternalAPIService.get_daily_prompt()
        return {
            "success": True,
            "data": prompt
        }
    except Exception as e:
        return {
            "success": False,
            "data": "What's on your mind today?"
        }


# Pixabay support removed
