"""
Supabase database service for interacting with tables
"""
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from supabase import Client
from app.core.database import get_supabase


class SupabaseService:
    """Base service class for Supabase operations"""
    
    def __init__(self):
        self.supabase: Client = get_supabase()
    
    def generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())


class UserService(SupabaseService):
    """Service for user operations"""
    
    def get_user_by_clerk_id(self, clerk_user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by Clerk user ID"""
        try:
            result = self.supabase.table("users").select("*").eq("clerk_user_id", clerk_user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user by clerk ID: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by internal ID"""
        try:
            result = self.supabase.table("users").select("*").eq("id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            user_data["id"] = self.generate_id()
            user_data["created_at"] = datetime.now().isoformat()
            user_data["updated_at"] = datetime.now().isoformat()
            
            print(f"Debug - create_user called with data: {user_data}")
            
            # Ensure email is not None
            if not user_data.get("email"):
                clerk_user_id = user_data.get("clerk_user_id", "unknown")
                user_data["email"] = f"{clerk_user_id}@clerk.placeholder"
                print(f"Debug - No email provided, setting placeholder: {user_data['email']}")
            
            print(f"Debug - Final user_data before insert: {user_data}")
            
            result = self.supabase.table("users").insert(user_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            # Graceful fallback for local dev when Supabase is unreachable.
            # Return an ephemeral, in-memory user object so the app can continue.
            print(f"Error creating user (fallback to in-memory): {e}")
            return {
                "id": user_data.get("id") or self.generate_id(),
                "clerk_user_id": user_data.get("clerk_user_id"),
                "email": user_data.get("email"),
                "name": user_data.get("name") or "User",
                "image_url": user_data.get("image_url"),
                "created_at": user_data.get("created_at") or datetime.now().isoformat(),
                "updated_at": user_data.get("updated_at") or datetime.now().isoformat(),
                "__ephemeral": True,
            }
    
    def get_or_create_user(self, clerk_user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get existing user or create new one"""
        user = self.get_user_by_clerk_id(clerk_user_id)
        if user:
            return user
        
        # Create new user with data from Clerk API
        create_data = {
            "clerk_user_id": clerk_user_id,
            "email": user_data.get("email") or f"{clerk_user_id}@clerk.placeholder",
            "name": user_data.get("name") or "User",
            "image_url": user_data.get("image_url")
        }
        return self.create_user(create_data)


class CollectionService(SupabaseService):
    """Service for collection operations"""
    
    def get_collections(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all collections for a user"""
        try:
            result = self.supabase.table("collections").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting collections (fallback to empty list): {e}")
            # Return a deterministic empty list rather than 500 for unreachable DB in dev
            return []
    
    def create_collection(self, user_id: str, collection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new collection"""
        try:
            data = {
                "id": self.generate_id(),
                "user_id": user_id,
                "name": collection_data["name"],
                "description": collection_data.get("description"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("collections").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating collection (dev fallback): {e}")
            # Dev fallback: echo back the object so UI doesn't crash; mark ephemeral
            return {**data, "__ephemeral": True}
    
    def update_collection(self, collection_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a collection"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("collections").update(update_data).eq("id", collection_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating collection (dev fallback): {e}")
            return {"id": collection_id, **update_data, "user_id": user_id, "__ephemeral": True}
    
    def delete_collection(self, collection_id: str, user_id: str) -> bool:
        """Delete a collection"""
        try:
            result = self.supabase.table("collections").delete().eq("id", collection_id).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting collection (dev fallback): {e}")
            return True
    
    def get_collection(self, collection_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific collection"""
        try:
            result = self.supabase.table("collections").select("*").eq("id", collection_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting collection (dev fallback): {e}")
            return None


class EntryService(SupabaseService):
    """Service for journal entry operations"""
    
    async def create_entry(self, user_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new journal entry with embedding generation"""
        try:
            data = {
                "id": self.generate_id(),
                "user_id": user_id,
                "title": entry_data["title"],
                "content": entry_data["content"],
                "mood": entry_data["mood"],
                "mood_score": entry_data["mood_score"],
                "mood_image_url": entry_data.get("mood_image_url"),
                "collection_id": entry_data.get("collection_id"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Generate embedding for the entry content
            try:
                from app.services.embedding_service import embedding_service
                full_content = f"{entry_data['title']} {entry_data['content']}"
                embedding = await embedding_service.generate_embedding(full_content)
                if embedding:
                    data["content_embedding"] = embedding
            except Exception as e:
                print(f"Warning: Failed to generate embedding: {e}")
                # Continue without embedding - can be generated later
            
            result = self.supabase.table("entries").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating entry: {e}")
            raise Exception(f"Failed to create entry: {str(e)}")
    
    def create_entry_sync(self, user_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous version of create_entry for backward compatibility"""
        try:
            data = {
                "id": self.generate_id(),
                "user_id": user_id,
                "title": entry_data["title"],
                "content": entry_data["content"],
                "mood": entry_data["mood"],
                "mood_score": entry_data["mood_score"],
                "mood_image_url": entry_data.get("mood_image_url"),
                "collection_id": entry_data.get("collection_id"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("entries").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating entry: {e}")
            raise Exception(f"Failed to create entry: {str(e)}")
    
    def get_entries(self, user_id: str, collection_id: Optional[str] = None, order_by: str = "desc") -> List[Dict[str, Any]]:
        """Get journal entries for a user"""
        try:
            query = self.supabase.table("entries").select("*, collections(id, name)").eq("user_id", user_id)
            
            if collection_id == "unorganized" or collection_id is None:
                query = query.is_("collection_id", "null")
            elif collection_id:
                query = query.eq("collection_id", collection_id)
            
            if order_by == "asc":
                query = query.order("created_at", desc=False)
            else:
                query = query.order("created_at", desc=True)
            
            result = query.execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting entries: {e}")
            return []
    
    def get_entry(self, entry_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific entry"""
        try:
            result = self.supabase.table("entries").select("*, collections(id, name)").eq("id", entry_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting entry: {e}")
            return None
    
    async def update_entry(self, entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a journal entry and regenerate embedding if content changed"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            
            # If content or title changed, regenerate embedding
            if "content" in update_data or "title" in update_data:
                try:
                    # Get current entry to build full content
                    current_entry = self.get_entry(entry_id, user_id)
                    if current_entry:
                        new_title = update_data.get("title", current_entry.get("title", ""))
                        new_content = update_data.get("content", current_entry.get("content", ""))
                        full_content = f"{new_title} {new_content}"
                        
                        from app.services.embedding_service import embedding_service
                        embedding = await embedding_service.generate_embedding(full_content)
                        if embedding:
                            update_data["content_embedding"] = embedding
                except Exception as e:
                    print(f"Warning: Failed to update embedding: {e}")
            
            result = self.supabase.table("entries").update(update_data).eq("id", entry_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating entry: {e}")
            raise Exception(f"Failed to update entry: {str(e)}")
    
    def update_entry_sync(self, entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous version of update_entry for backward compatibility"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("entries").update(update_data).eq("id", entry_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating entry: {e}")
            raise Exception(f"Failed to update entry: {str(e)}")
    
    def delete_entry(self, entry_id: str, user_id: str) -> bool:
        """Delete a journal entry"""
        try:
            result = self.supabase.table("entries").delete().eq("id", entry_id).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting entry: {e}")
            raise Exception(f"Failed to delete entry: {str(e)}")


class DraftService(SupabaseService):
    """Service for draft operations"""
    
    def get_draft(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get current draft for a user"""
        try:
            result = self.supabase.table("drafts").select("*").eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting draft: {e}")
            return None
    
    def save_draft(self, user_id: str, draft_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update draft for a user"""
        try:
            # Check if draft exists
            existing_draft = self.get_draft(user_id)
            
            if existing_draft:
                # Update existing draft
                update_data = {
                    **draft_data,
                    "updated_at": datetime.now().isoformat()
                }
                result = self.supabase.table("drafts").update(update_data).eq("user_id", user_id).execute()
                return result.data[0] if result.data else None
            else:
                # Create new draft
                data = {
                    "id": self.generate_id(),
                    "user_id": user_id,
                    **draft_data,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                result = self.supabase.table("drafts").insert(data).execute()
                return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error saving draft: {e}")
            raise Exception(f"Failed to save draft: {str(e)}")
    
    def delete_draft(self, user_id: str) -> bool:
        """Delete draft for a user"""
        try:
            result = self.supabase.table("drafts").delete().eq("user_id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting draft: {e}")
            return False
