# tests/test_schemas.py

import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas import UserCreate, UserLogin, UserResponse

# ============================================================================================
# UserCreate Schema Tests
# ============================================================================================

def test_user_create_valid():
    """Test the valid UserCreate schema."""
    user_data = {
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password": "SecurePass123"
    }
    user = UserCreate(**user_data)
    assert user.username == "johndoe"
    assert user.email == "john.doe@example.com"
    assert user.password == "SecurePass123"

def test_user_create_invalid_email():
    """Test the invalid email format in UserCreate schema."""
    user_data = {
        "username": "johndoe",
        "email": "invalid-email",
        "password": "SecurePass123"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_create_invalid_password():
    """Test the invalid password format in UserCreate schema."""
    user_data = {
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password": "short"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

# ============================================================================================
# UserLogin Schema Tests
# ============================================================================================

def test_user_login_valid():
    """Test the valid UserLogin schema."""
    login_data = {
        "username": "johndoe",
        "password": "SecurePass123"
    }
    login = UserLogin(**login_data)
    assert login.username == "johndoe"
    assert login.password == "SecurePass123"

def test_user_login_missing_password():
    """Test the missing password in UserLogin schema."""
    login_data = {
        "username": "johndoe",
    }
    with pytest.raises(ValidationError):
        UserLogin(**login_data)

# ============================================================================================
# UserResponse Schema Tests
# ============================================================================================

def test_user_response_valid():
    """Test the valid UserResponse schema."""
    user_data = {
        "id": uuid4(),
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password_hash": "hashed_password",
        "created_at": datetime.utcnow()
    }
    user_response = UserResponse(**user_data)
    assert user_response.id is not None
    assert user_response.username == "johndoe"
    assert user_response.email == "john.doe@example.com"
    assert isinstance(user_response.created_at, datetime)

def test_user_response_invalid_data():
    """Test invalid data (missing required fields) in UserResponse schema."""
    user_data = {
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password_hash": "hashed_password"
    }
    with pytest.raises(ValidationError):
        UserResponse(**user_data)
