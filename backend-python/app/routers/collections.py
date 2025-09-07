from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.middleware import get_current_user, limiter
from app.schemas import Collection as CollectionSchema, CollectionCreate, CollectionUpdate, StandardResponse
from app.services.supabase_service import UserService, CollectionService

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/", response_model=List[CollectionSchema])
@limiter.limit("60/minute")
async def get_collections(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all collections for the authenticated user
    """
    user_service = UserService()
    user = user_service.get_or_create_user(current_user["user_id"], current_user)

    collection_service = CollectionService()
    collections = collection_service.get_collections(user["id"])

    return collections


@router.post("/", response_model=CollectionSchema)
@limiter.limit("10/hour")  # Stricter rate limit for creation
async def create_collection(
    request: Request,
    collection_data: CollectionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new collection for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_or_create_user(current_user["user_id"], current_user)

        collection_service = CollectionService()
        collection = collection_service.create_collection(
            user["id"],
            collection_data.model_dump()
        )

        if not collection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create collection"
            )

        return collection

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create collection: {str(e)}"
        )


@router.put("/{collection_id}", response_model=CollectionSchema)
@limiter.limit("30/minute")
async def update_collection(
    request: Request,
    collection_id: str,
    collection_data: CollectionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a collection for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_or_create_user(current_user["user_id"], current_user)

        collection_service = CollectionService()
        
        # Check if collection exists
        existing_collection = collection_service.get_collection(collection_id, user["id"])
        if not existing_collection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not found"
            )

        update_data = collection_data.model_dump(exclude_unset=True)
        collection = collection_service.update_collection(
            collection_id,
            user["id"],
            update_data
        )

        if not collection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update collection"
            )

        return collection

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update collection: {str(e)}"
        )


@router.delete("/{collection_id}", response_model=StandardResponse)
@limiter.limit("30/minute")
async def delete_collection(
    request: Request,
    collection_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a collection for the authenticated user
    """
    try:
        user_service = UserService()
        user = user_service.get_or_create_user(current_user["user_id"], current_user)

        collection_service = CollectionService()
        
        # Check if collection exists
        existing_collection = collection_service.get_collection(collection_id, user["id"])
        if not existing_collection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not found"
            )

        success = collection_service.delete_collection(collection_id, user["id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete collection"
            )

        return StandardResponse(success=True, data={"message": "Collection deleted successfully"})

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete collection: {str(e)}"
        )
