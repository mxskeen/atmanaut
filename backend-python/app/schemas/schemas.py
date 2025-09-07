"""
Pydantic schemas for request/response models
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Base schemas
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    image_url: Optional[str] = None


class UserCreate(UserBase):
    clerk_user_id: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None


class User(UserBase):
    id: str
    clerk_user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Collection schemas
class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Collection(CollectionBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CollectionWithEntries(Collection):
    entries: List["Entry"] = []


# Entry schemas
class EntryBase(BaseModel):
    title: str
    content: str
    mood: str
    mood_score: int
    mood_image_url: Optional[str] = None
    collection_id: Optional[str] = None


class EntryCreate(BaseModel):
    title: str
    content: str
    mood: str
    moodQuery: str  # For fetching Pixabay image - matches frontend camelCase
    collectionId: Optional[str] = None  # Matches frontend camelCase


class EntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None
    moodQuery: Optional[str] = None  # Matches frontend camelCase
    collectionId: Optional[str] = None  # Matches frontend camelCase


class Entry(EntryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    collection: Optional[Collection] = None
    
    class Config:
        from_attributes = True


class EntryWithMoodData(Entry):
    mood_data: dict


# Draft schemas
class DraftBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None


class DraftCreate(DraftBase):
    pass


class DraftUpdate(DraftBase):
    pass


class Draft(DraftBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Analytics schemas
class AnalyticsTimelineItem(BaseModel):
    date: str
    average_score: float
    entry_count: int


class AnalyticsStats(BaseModel):
    total_entries: int
    average_score: float
    most_frequent_mood: Optional[str]
    daily_average: float


class AnalyticsResponse(BaseModel):
    success: bool
    data: dict = Field(default_factory=dict)


# Response schemas
class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None


class EntryListResponse(BaseModel):
    success: bool
    data: dict


class StandardResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


# Update forward references
CollectionWithEntries.model_rebuild()
