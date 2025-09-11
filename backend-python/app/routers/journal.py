from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from app.middleware import get_current_user, limiter
from app.schemas import (
    Entry as EntrySchema, EntryCreate, EntryUpdate, 
    EntryListResponse, StandardResponse,
    Draft as DraftSchema, DraftCreate, DraftUpdate
)
from app.services.supabase_service import UserService, EntryService, DraftService, CollectionService
from app.services.external_api_service import ExternalAPIService
from app.services.mood_service import get_mood_by_key, get_mood_by_id

router = APIRouter(prefix="/journal", tags=["journal"])


@router.post("/entries", response_model=EntrySchema)
@limiter.limit("20/hour")  # Rate limit for entry creation
async def create_journal_entry(
    request: Request,
    entry_data: EntryCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new journal entry for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Get mood data
        mood = get_mood_by_key(entry_data.mood)
        if not mood:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid mood"
            )

        # Get mood image from Pixabay
        mood_image_url = await ExternalAPIService.get_pixabay_image(entry_data.moodQuery)

        # Validate collection if provided
        collection_id = None
        if entry_data.collectionId and entry_data.collectionId.strip():
            collection_service = CollectionService()
            collection = collection_service.get_collection(entry_data.collectionId, user["id"])
            if not collection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Collection not found"
                )
            collection_id = entry_data.collectionId

        # Create the entry
        entry_service = EntryService()
        entry_data_dict = {
            "title": entry_data.title,
            "content": entry_data.content,
            "mood": mood["id"],
            "mood_score": mood["score"],
            "mood_image_url": mood_image_url,
            "collection_id": collection_id
        }

        # Use async method to create entry with embedding generation
        try:
            entry = await entry_service.create_entry(user["id"], entry_data_dict)
        except Exception as e:
            print(f"Failed to create entry with embedding, falling back to sync method: {e}")
            entry = entry_service.create_entry_sync(user["id"], entry_data_dict)
        
        # Delete existing draft after successful publication
        draft_service = DraftService()
        draft_service.delete_draft(user["id"])

        return entry

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create entry: {str(e)}"
        )


@router.get("/entries", response_model=EntryListResponse)
@limiter.limit("60/minute")
async def get_journal_entries(
    request: Request,
    collection_id: Optional[str] = Query(None),
    order_by: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get journal entries for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Get entries
        entry_service = EntryService()
        entries = entry_service.get_entries(user["id"], collection_id, order_by)

        # Add mood data to each entry and convert to camelCase for frontend
        entries_with_mood_data = []
        for entry in entries:
            # Convert snake_case to camelCase for frontend compatibility
            entry_dict = {
                "id": entry["id"],
                "title": entry["title"],
                "content": entry["content"],
                "mood": entry["mood"],
                "moodScore": entry["mood_score"],
                "moodImageUrl": entry["mood_image_url"],
                "collectionId": entry["collection_id"],
                "createdAt": entry["created_at"],
                "updatedAt": entry["updated_at"],
                "userId": entry["user_id"],
                "moodData": get_mood_by_id(entry["mood"])
            }
            entries_with_mood_data.append(entry_dict)

        return EntryListResponse(
            success=True,
            data={
                "entries": entries_with_mood_data
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get entries: {str(e)}"
        )


@router.get("/entries/collection/{collection_id}", response_model=EntryListResponse)
@limiter.limit("60/minute")
async def get_collection_entries(
    request: Request,
    collection_id: str,
    order_by: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get journal entries for a specific collection
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Handle special cases
        entry_service = EntryService()
        
        if collection_id == "all":
            # Return all entries for the user
            entries = entry_service.get_entries(user["id"], None, order_by)
        elif collection_id == "unorganized":
            # Return entries without collection
            entries = entry_service.get_entries(user["id"], "unorganized", order_by)
        else:
            # Verify collection exists and belongs to user for real collections
            collection_service = CollectionService()
            collection = collection_service.get_collection(collection_id, user["id"])
            if not collection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Collection not found"
                )
            # Get entries for this specific collection
            entries = entry_service.get_entries(user["id"], collection_id, order_by)

        # Add mood data to each entry and convert to camelCase for frontend
        entries_with_mood_data = []
        for entry in entries:
            # Convert snake_case to camelCase for frontend compatibility
            entry_dict = {
                "id": entry["id"],
                "title": entry["title"],
                "content": entry["content"],
                "mood": entry["mood"],
                "moodScore": entry["mood_score"],
                "moodImageUrl": entry["mood_image_url"],
                "collectionId": entry["collection_id"],
                "createdAt": entry["created_at"],
                "updatedAt": entry["updated_at"],
                "userId": entry["user_id"],
                "moodData": get_mood_by_id(entry["mood"])
            }
            entries_with_mood_data.append(entry_dict)

        return EntryListResponse(
            success=True,
            data={
                "entries": entries_with_mood_data
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get collection entries: {str(e)}"
        )


@router.get("/entries/{entry_id}")
@limiter.limit("60/minute")
async def get_journal_entry(
    request: Request,
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific journal entry for the authenticated user
    """
    user_service = UserService()
    user = user_service.get_user_by_clerk_id(current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    entry_service = EntryService()
    entry = entry_service.get_entry(entry_id, user["id"])

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

    # Convert snake_case to camelCase for frontend compatibility
    entry_with_mood_data = {
        "id": entry["id"],
        "title": entry["title"],
        "content": entry["content"],
        "mood": entry["mood"],
        "moodScore": entry["mood_score"],
        "moodImageUrl": entry["mood_image_url"],
        "collectionId": entry["collection_id"],
        "createdAt": entry["created_at"],
        "updatedAt": entry["updated_at"],
        "userId": entry["user_id"],
        "moodData": get_mood_by_id(entry["mood"])
    }

    return entry_with_mood_data


@router.put("/entries/{entry_id}", response_model=EntrySchema)
@limiter.limit("30/minute")
async def update_journal_entry(
    request: Request,
    entry_id: str,
    entry_data: EntryUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a journal entry for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        entry_service = EntryService()
        entry = entry_service.get_entry(entry_id, user["id"])

        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entry not found"
            )

        # Prepare update data
        update_data = entry_data.model_dump(exclude_unset=True)
        
        # Handle mood update
        if "mood" in update_data:
            mood = get_mood_by_key(update_data["mood"])
            if not mood:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid mood"
                )
            
            # Get new mood image if mood changed or moodQuery provided
            if entry["mood"] != mood["id"] or entry_data.moodQuery:
                mood_query = entry_data.moodQuery or mood["pixabay_query"]
                mood_image_url = await ExternalAPIService.get_pixabay_image(mood_query)
                update_data["mood_image_url"] = mood_image_url
            
            update_data["mood"] = mood["id"]
            update_data["mood_score"] = mood["score"]
        
        # Convert camelCase to snake_case for database
        if "moodQuery" in update_data:
            del update_data["moodQuery"]  # Remove as it's not a model field
        if "collectionId" in update_data:
            update_data["collection_id"] = update_data.pop("collectionId")

        # Update the entry
        try:
            updated_entry = await entry_service.update_entry(entry_id, user["id"], update_data)
        except Exception as e:
            print(f"Failed to update entry with embedding, falling back to sync method: {e}")
            updated_entry = entry_service.update_entry_sync(entry_id, user["id"], update_data)

        return updated_entry

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update entry: {str(e)}"
        )


@router.delete("/entries/{entry_id}", response_model=StandardResponse)
@limiter.limit("30/minute")
async def delete_journal_entry(
    request: Request,
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a journal entry for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        entry_service = EntryService()
        entry = entry_service.get_entry(entry_id, user["id"])

        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entry not found"
            )

        success = entry_service.delete_entry(entry_id, user["id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete entry"
            )

        return StandardResponse(success=True, data={"message": "Entry deleted successfully"})

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete entry: {str(e)}"
        )


# Draft endpoints
@router.get("/draft", response_model=StandardResponse)
@limiter.limit("60/minute")
async def get_draft(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get current draft for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        draft_service = DraftService()
        draft = draft_service.get_draft(user["id"])

        return StandardResponse(
            success=True,
            data=draft
        )

    except Exception as e:
        return StandardResponse(
            success=False,
            error=str(e)
        )


@router.post("/draft", response_model=StandardResponse)
@limiter.limit("60/minute")
async def save_draft(
    request: Request,
    draft_data: DraftCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Save draft for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        draft_service = DraftService()
        draft = draft_service.save_draft(user["id"], draft_data.model_dump())

        return StandardResponse(
            success=True,
            data=draft
        )

    except Exception as e:
        return StandardResponse(
            success=False,
            error=str(e)
        )
