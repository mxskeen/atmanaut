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


@router.get("/pixabay-image")
@limiter.limit("50/hour")
async def get_pixabay_image(request: Request, query: str):
    """
    Get image from Pixabay API
    """
    try:
        image_url = await ExternalAPIService.get_pixabay_image(query)
        return {
            "success": True,
            "data": image_url
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }
