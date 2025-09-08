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
            # print(f"Error getting user by clerk ID: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by internal ID"""
        try:
            result = self.supabase.table("users").select("*").eq("id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            # print(f"Error getting user by ID: {e}")
            return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            user_data["id"] = self.generate_id()
            user_data["created_at"] = datetime.now().isoformat()
            user_data["updated_at"] = datetime.now().isoformat()
            
            # print(f"Debug - create_user called with data: {user_data}")

            # Ensure email is not None
            if not user_data.get("email"):
                clerk_user_id = user_data.get("clerk_user_id", "unknown")
                user_data["email"] = f"{clerk_user_id}@clerk.placeholder"
                # print(f"Debug - No email provided, setting placeholder: {user_data['email']}")

            # print(f"Debug - Final user_data before insert: {user_data}")
            
            result = self.supabase.table("users").insert(user_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            # print(f"Error creating user: {e}")
            raise Exception(f"Failed to create user: {str(e)}")
    
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
            # print(f"Error getting collections: {e}")
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
            # print(f"Error creating collection: {e}")
            raise Exception(f"Failed to create collection: {str(e)}")
    
    def update_collection(self, collection_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a collection"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("collections").update(update_data).eq("id", collection_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            # print(f"Error updating collection: {e}")
            raise Exception(f"Failed to update collection: {str(e)}")
    
    def delete_collection(self, collection_id: str, user_id: str) -> bool:
        """Delete a collection"""
        try:
            result = self.supabase.table("collections").delete().eq("id", collection_id).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            # print(f"Error deleting collection: {e}")
            raise Exception(f"Failed to delete collection: {str(e)}")
    
    def get_collection(self, collection_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific collection"""
        try:
            result = self.supabase.table("collections").select("*").eq("id", collection_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            # print(f"Error getting collection: {e}")
            return None


class EntryService(SupabaseService):
    def create_future_entry(self, user_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new future journal entry"""
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
                "send_to_future_date": entry_data.get("send_to_future_date"),
                "is_future_entry": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            result = self.supabase.table("entries").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            # print(f"Error creating future entry: {e}")
            raise Exception(f"Failed to create future entry: {str(e)}")

    def get_due_future_entries(self, user_id: str) -> list:
        """Get all future entries due today for a user and not yet delivered"""
        try:
            today = datetime.utcnow().date().isoformat()
            result = self.supabase.table("entries") \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("is_future_entry", True) \
                .is_("delivered_at", "null") \
                .gte("send_to_future_date", today + "T00:00:00Z") \
                .lte("send_to_future_date", today + "T23:59:59Z") \
                .execute()
            return result.data or []
        except Exception as e:
            return []

    def mark_entry_delivered(self, entry_id: str, user_id: str) -> bool:
        """Mark a future entry as delivered"""
        try:
            now = datetime.now().isoformat()
            result = self.supabase.table("entries") \
                .update({"delivered_at": now}) \
                .eq("id", entry_id) \
                .eq("user_id", user_id) \
                .execute()
            return True
        except Exception as e:
            return False

    def update_future_date(self, entry_id: str, user_id: str, new_date: str) -> bool:
        """Update the send_to_future_date for a future entry"""
        try:
            result = self.supabase.table("entries") \
                .update({"send_to_future_date": new_date, "updated_at": datetime.now().isoformat()}) \
                .eq("id", entry_id) \
                .eq("user_id", user_id) \
                .execute()
            return True
        except Exception as e:
            return False
    """Service for journal entry operations"""
    
    def create_entry(self, user_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new journal entry"""
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
            return []
    
    def get_entry(self, entry_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific entry"""
        try:
            result = self.supabase.table("entries").select("*, collections(id, name)").eq("id", entry_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None
    
    def update_entry(self, entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a journal entry"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("entries").update(update_data).eq("id", entry_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Failed to update entry: {str(e)}")
    
    def delete_entry(self, entry_id: str, user_id: str) -> bool:
        """Delete a journal entry"""
        try:
            result = self.supabase.table("entries").delete().eq("id", entry_id).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete entry: {str(e)}")


class DraftService(SupabaseService):
    """Service for draft operations"""
    
    def get_draft(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get current draft for a user"""
        try:
            result = self.supabase.table("drafts").select("*").eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
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
            raise Exception(f"Failed to save draft: {str(e)}")
    
    def delete_draft(self, user_id: str) -> bool:
        """Delete draft for a user"""
        try:
            result = self.supabase.table("drafts").delete().eq("user_id", user_id).execute()
            return True
        except Exception as e:
            return False
