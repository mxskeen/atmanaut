from fastapi import Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


def get_user_id_or_ip(request: Request):
    """
    Get user ID from auth token or fall back to IP address for rate limiting
    """
    try:
        # Try to get user ID from auth header if available
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            # Extract user ID from token (simplified)
            return authorization.split()[1][:20]  # Use first 20 chars as identifier
    except Exception:
        pass
    
    # Fall back to IP address
    return get_remote_address(request)


# Create limiter instance with memory storage
limiter = Limiter(
    key_func=get_user_id_or_ip,
    storage_uri="memory://",
)


def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom rate limit exceeded handler
    """
    response = {
        "error": "Rate limit exceeded",
        "detail": f"Rate limit exceeded: {exc.detail}",
        "retry_after": getattr(exc, 'retry_after', 60)
    }
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=response
    )
