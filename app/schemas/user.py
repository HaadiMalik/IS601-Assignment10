from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    """Schema for user response data"""
    id: UUID
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime

    class Config:
        orm_mode = True  # Allows compatibility with ORM models like SQLAlchemy