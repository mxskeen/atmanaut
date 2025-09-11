from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.middleware import get_current_user, limiter
from app.schemas import (
    SemanticSearchRequest, HybridSearchRequest, SearchResponse, 
    SearchResultEntry, EmbeddingUpdateResponse, StandardResponse
)
from app.services.supabase_service import UserService
from app.services.semantic_search_service import semantic_search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/semantic", response_model=SearchResponse)
@limiter.limit("30/minute")  # Rate limit for search
async def semantic_search(
    request: Request,
    search_request: SemanticSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Perform semantic search on journal entries
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Parse date range if provided
        date_range = None
        if search_request.start_date or search_request.end_date:
            start_date = datetime.fromisoformat(search_request.start_date) if search_request.start_date else None
            end_date = datetime.fromisoformat(search_request.end_date) if search_request.end_date else None
            if start_date or end_date:
                date_range = (start_date, end_date)

        # Perform semantic search
        results = await semantic_search_service.search_entries(
            user_id=user["id"],
            query=search_request.query,
            limit=search_request.limit,
            similarity_threshold=search_request.similarity_threshold,
            date_range=date_range,
            mood_filter=search_request.mood_filter,
            collection_id=search_request.collection_id
        )

        # Convert results to response format
        search_results = []
        for result in results:
            search_result = SearchResultEntry(
                id=result["id"],
                title=result["title"],
                content=result["content"],
                mood=result["mood"],
                mood_score=result["mood_score"],
                mood_image_url=result.get("mood_image_url"),
                collection_id=result.get("collection_id"),
                user_id=result["user_id"],
                created_at=datetime.fromisoformat(result["created_at"]),
                updated_at=datetime.fromisoformat(result["updated_at"]),
                similarity_score=result.get("similarity_score")
            )
            search_results.append(search_result)

        return SearchResponse(
            success=True,
            query=search_request.query,
            total_results=len(search_results),
            results=search_results,
            search_type="semantic"
        )

    except Exception as e:
        print(f"Error in semantic search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/hybrid", response_model=SearchResponse)
@limiter.limit("30/minute")  # Rate limit for search
async def hybrid_search(
    request: Request,
    search_request: HybridSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Perform hybrid search (semantic + keyword) on journal entries
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Parse date range if provided
        date_range = None
        if search_request.start_date or search_request.end_date:
            start_date = datetime.fromisoformat(search_request.start_date) if search_request.start_date else None
            end_date = datetime.fromisoformat(search_request.end_date) if search_request.end_date else None
            if start_date or end_date:
                date_range = (start_date, end_date)

        # Perform hybrid search
        results = await semantic_search_service.hybrid_search_entries(
            user_id=user["id"],
            query=search_request.query,
            limit=search_request.limit,
            semantic_weight=search_request.semantic_weight,
            keyword_weight=search_request.keyword_weight,
            date_range=date_range,
            mood_filter=search_request.mood_filter,
            collection_id=search_request.collection_id
        )

        # Convert results to response format
        search_results = []
        for result in results:
            search_result = SearchResultEntry(
                id=result["id"],
                title=result["title"],
                content=result["content"],
                mood=result["mood"],
                mood_score=result["mood_score"],
                mood_image_url=result.get("mood_image_url"),
                collection_id=result.get("collection_id"),
                user_id=result["user_id"],
                created_at=datetime.fromisoformat(result["created_at"]),
                updated_at=datetime.fromisoformat(result["updated_at"]),
                similarity_score=result.get("semantic_score"),
                keyword_score=result.get("keyword_score"),
                combined_score=result.get("combined_score")
            )
            search_results.append(search_result)

        return SearchResponse(
            success=True,
            query=search_request.query,
            total_results=len(search_results),
            results=search_results,
            search_type="hybrid"
        )

    except Exception as e:
        print(f"Error in hybrid search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/embeddings/update", response_model=EmbeddingUpdateResponse)
@limiter.limit("2/hour")  # Rate limit for batch updates
async def update_embeddings(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Update embeddings for all user entries that don't have them
    """
    try:
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update embeddings for entries without them
        updated_count = await semantic_search_service.batch_update_embeddings(user["id"])

        return EmbeddingUpdateResponse(
            success=True,
            entries_updated=updated_count,
            message=f"Successfully updated embeddings for {updated_count} entries"
        )

    except Exception as e:
        print(f"Error updating embeddings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update embeddings: {str(e)}"
        )


@router.get("/suggestions")
@limiter.limit("20/minute")
async def search_suggestions(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get search suggestions based on common queries
    """
    suggestions = [
        "What was my worst day this month?",
        "Show me entries about happiness",
        "Find sad entries from last week", 
        "What made me anxious in September?",
        "Show me my most positive moments",
        "Find entries about work stress",
        "What was I grateful for this week?",
        "Show me entries when I felt lonely",
        "Find my best day last month",
        "What made me excited recently?"
    ]
    
    return {
        "success": True,
        "suggestions": suggestions
    }
