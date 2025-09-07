from supabase import create_client, Client
from app.core.config import settings

# Create Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_anon_key)


def get_supabase():
    """
    Dependency to get Supabase client
    """
    return supabase
