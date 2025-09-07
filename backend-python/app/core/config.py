from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Supabase
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_anon_key: str = Field(..., env="SUPABASE_ANON_KEY")
    
    # Clerk Authentication
    clerk_secret_key: str = Field(..., env="CLERK_SECRET_KEY")
    clerk_publishable_key: str = Field(..., env="CLERK_PUBLISHABLE_KEY")
    
    # External APIs
    pixabay_api_key: str = Field(..., env="PIXABAY_API_KEY")
    
    # CORS
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Rate limiting
    rate_limit_requests: int = Field(default=10, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # 1 hour
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    app_name: str = "Atmanaut Backend"
    debug: bool = Field(default=False, env="DEBUG")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
