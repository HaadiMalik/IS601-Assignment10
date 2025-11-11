from pydantic import BaseModel, EmailStr, Field, model_validator
from uuid import UUID

class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(min_length=3, max_length=50, example="johndoe")
    email: EmailStr = Field(example="john.doe@example.com")

    class Config:
        orm_mode = True  # Allows compatibility with ORM models like SQLAlchemy


class PasswordMixin(BaseModel):
    """Mixin for password validation"""
    password: str = Field(min_length=6, max_length=128, example="SecurePass123")

    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, values: dict) -> dict:
        password = values.get("password")
        if not password:
            raise ValueError("Password is required")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        return values


class UserCreate(UserBase, PasswordMixin):
    """Schema for user creation"""
    pass


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(min_length=3, max_length=50, example="johndoe")
    password: str = Field(min_length=6, max_length=128, example="SecurePass123")
