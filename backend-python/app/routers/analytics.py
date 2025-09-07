"""
Analytics API router
"""
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.middleware import get_current_user, limiter
from app.schemas import AnalyticsResponse
from app.services.supabase_service import UserService, EntryService
from app.services.mood_service import get_mood_by_id

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/", response_model=AnalyticsResponse)
@limiter.limit("30/minute")
async def get_analytics(
    request: Request,
    period: str = "30d",
    current_user: dict = Depends(get_current_user)
):
    """
    Get analytics data for the authenticated user
    """
    try:
        # Get user from Supabase
        user_service = UserService()
        user = user_service.get_user_by_clerk_id(current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Calculate start date based on period
        start_date = datetime.now()
        if period == "7d":
            start_date = start_date - timedelta(days=7)
        elif period == "15d":
            start_date = start_date - timedelta(days=15)
        elif period == "30d":
            start_date = start_date - timedelta(days=30)
        else:
            start_date = start_date - timedelta(days=30)

        start_date_str = start_date.isoformat()

        # Get entries for the period using Supabase
        entry_service = EntryService()
        all_entries = entry_service.get_entries(user["id"])
        
        # Filter entries by date (since Supabase query might not support date filtering directly)
        entries = []
        for entry in all_entries:
            try:
                # Handle different date formats that might come from the database
                created_at = entry["created_at"]
                if isinstance(created_at, str):
                    # Remove timezone suffix and parse
                    created_at_clean = created_at.replace('Z', '+00:00')
                    entry_date = datetime.fromisoformat(created_at_clean)
                else:
                    # If it's already a datetime object
                    entry_date = created_at
                
                if entry_date >= start_date:
                    entries.append(entry)
            except (ValueError, TypeError) as e:
                # Skip entries with invalid dates
                print(f"Skipping entry with invalid date: {entry.get('created_at')}, error: {e}")
                continue

        # Process entries for analytics
        mood_data = {}
        for entry in entries:
            try:
                # Handle different date formats
                created_at = entry["created_at"]
                if isinstance(created_at, str):
                    created_at_clean = created_at.replace('Z', '+00:00')
                    entry_date = datetime.fromisoformat(created_at_clean)
                else:
                    entry_date = created_at
                
                date_str = entry_date.strftime("%Y-%m-%d")
                if date_str not in mood_data:
                    mood_data[date_str] = {
                        "total_score": 0,
                        "count": 0,
                        "entries": []
                    }
                mood_data[date_str]["total_score"] += entry.get("mood_score", 0)
                mood_data[date_str]["count"] += 1
                mood_data[date_str]["entries"].append(entry)
            except (ValueError, TypeError) as e:
                print(f"Skipping entry in mood processing: {entry.get('id')}, error: {e}")
                continue

        # Calculate averages and format data for charts
        timeline_data = []
        for date_str, data in mood_data.items():
            timeline_data.append({
                "date": date_str,
                "average_score": round(data["total_score"] / data["count"], 1),
                "entry_count": data["count"]
            })

        # Sort timeline data by date
        timeline_data.sort(key=lambda x: x["date"])

        # Calculate overall statistics
        total_entries = len(entries)
        if total_entries > 0:
            # Calculate average score, handling missing mood_score values
            valid_scores = [entry.get("mood_score", 0) for entry in entries if entry.get("mood_score") is not None]
            average_score = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else 0
            
            # Find most frequent mood
            mood_counts = {}
            for entry in entries:
                mood = entry.get("mood")
                if mood:
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1
            most_frequent_mood = max(mood_counts, key=mood_counts.get) if mood_counts else None
            
            # Calculate daily average
            days = 7 if period == "7d" else 15 if period == "15d" else 30
            daily_average = round(total_entries / days, 1)
        else:
            average_score = 0
            most_frequent_mood = None
            daily_average = 0

        overall_stats = {
            "total_entries": total_entries,
            "average_score": average_score,
            "most_frequent_mood": most_frequent_mood,
            "daily_average": daily_average,
        }

        return AnalyticsResponse(
            success=True,
            data={
                "timeline": timeline_data,
                "stats": overall_stats,
                "entries": [
                    {
                        **entry,
                        "mood_data": get_mood_by_id(entry.get("mood")) if entry.get("mood") else None
                    } for entry in entries
                ]
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics: {str(e)}"
        )
