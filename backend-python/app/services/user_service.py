"""
User service for user-related operations
"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.schemas import UserCreate, UserUpdate
from fastapi import HTTPException, status


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def get_user_by_clerk_id(db: Session, clerk_user_id: str) -> User:
        """Get user by Clerk user ID"""
        return db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by internal ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            user = User(
                id=str(uuid.uuid4()),
                clerk_user_id=user_data.clerk_user_id,
                email=user_data.email,
                name=user_data.name,
                image_url=user_data.image_url
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate) -> User:
        """Update user information"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_or_create_user(db: Session, clerk_user_id: str, user_data: dict) -> User:
        """Get existing user or create new one"""
        user = UserService.get_user_by_clerk_id(db, clerk_user_id)
        if user:
            return user
        
        # Create new user
        user_create = UserCreate(
            clerk_user_id=clerk_user_id,
            email=user_data.get("email"),
            name=user_data.get("name"),
            image_url=user_data.get("image_url")
        )
        return UserService.create_user(db, user_create)
