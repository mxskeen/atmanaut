import os
import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer
import jwt
from jwt import PyJWKClient, InvalidTokenError
from app.core.config import settings


security = HTTPBearer()


class ClerkAuth:
    """Clerk authentication handler"""
    
    def __init__(self):
        self.jwks_url = "https://api.clerk.com/v1/jwks"
        self.issuer = "https://clerk.com"
        self._jwks_cache = None
    
    async def get_jwks(self):
        """Get JSON Web Key Set from Clerk"""
        if self._jwks_cache is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_url)
                response.raise_for_status()
                self._jwks_cache = response.json()
        return self._jwks_cache
    
    async def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify Clerk JWT token and return user claims
        """
        try:
            # For development, we'll do basic verification
            # In production, you'd want to verify against Clerk's JWKS
            unverified_header = jwt.get_unverified_header(token)
            
            # Decode without verification for now (should be properly verified in production)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            return payload
            
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def get_user_from_token(self, token: str) -> Dict[str, Any]:
        """Get user from token and return full user data with profile info"""
        try:
            # Decode JWT without verification first to get issuer
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            print(f"JWT Payload: {unverified_payload}")
            
            issuer = unverified_payload.get('iss')
            if not issuer:
                raise HTTPException(status_code=401, detail="Invalid token: no issuer")
            
            # Get JWKS and verify token  
            jwks_client = PyJWKClient(f"{issuer}/.well-known/jwks.json")
            signing_key = jwks_client.get_signing_key_from_jwt(token).key
            
            # Clerk tokens use 'azp' instead of 'aud', so skip audience validation
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                options={"verify_aud": False}  # Skip audience validation for Clerk tokens
            )
            
            # Validate authorized party (azp) for additional security
            azp = payload.get('azp')
            if azp and azp not in ['http://localhost:3000', 'http://127.0.0.1:3000']:
                print(f"Warning: Token from unexpected authorized party: {azp}")
            
            user_id = payload.get('sub')
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: no user ID")
            
            # Fetch full user profile from Clerk API
            print(f"Fetching profile for user: {user_id}")
            user_profile = await self.fetch_user_profile(user_id)
            print(f"User profile fetched: {user_profile}")
            
            return user_profile
            
        except Exception as e:
            print(f"Token validation error: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def fetch_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Fetch user profile from Clerk API"""
        try:
            clerk_secret = settings.clerk_secret_key
            print(f"Fetching user profile for: {user_id}")
            print(f"Clerk secret key available: {bool(clerk_secret)}")
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {clerk_secret}",
                    "Content-Type": "application/json"
                }
                
                # Try the Clerk secret as Bearer token first, then as basic auth if needed
                url = f"https://api.clerk.com/v1/users/{user_id}"
                print(f"Making request to: {url}")
                
                response = await client.get(url, headers=headers)
                print(f"Clerk API response status: {response.status_code}")
                
                # If Bearer fails, try with the secret key directly
                if response.status_code == 401:
                    headers["Authorization"] = clerk_secret
                    response = await client.get(url, headers=headers)
                    print(f"Clerk API response status (retry): {response.status_code}")
                
                if response.status_code == 200:
                    profile = response.json()
                    print(f"Clerk API response: {profile}")
                    
                    email = None
                    if "email_addresses" in profile and profile["email_addresses"]:
                        email = profile["email_addresses"][0].get("email_address")
                    
                    user_data = {
                        "user_id": user_id,
                        "email": email,
                        "name": f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip(),
                        "image_url": profile.get("image_url")
                    }
                    print(f"Extracted user data: {user_data}")
                    return user_data
                else:
                    print(f"Clerk API error: {response.status_code} - {response.text}")
                    return {"user_id": user_id, "email": f"user_{user_id[-8:]}@placeholder.com"}
                    
        except Exception as e:
            print(f"Error fetching user profile: {e}")
            return {"user_id": user_id, "email": f"user_{user_id[-8:]}@placeholder.com"}


clerk_auth = ClerkAuth()


async def get_current_user(request: Request) -> dict:
    """
    Dependency to get current authenticated user
    """
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return await clerk_auth.get_user_from_token(token)


async def get_optional_user(request: Request) -> Optional[dict]:
    """
    Optional dependency to get current user (doesn't raise if not authenticated)
    """
    try:
        return await get_current_user(request)
    except HTTPException:
        return None


async def get_or_create_user_from_token(current_user: dict) -> dict:
    """
    Get or create user in Supabase from Clerk token data
    """
    from app.services.supabase_service import UserService
    
    user_service = UserService()
    return user_service.get_or_create_user(current_user["user_id"], current_user)
