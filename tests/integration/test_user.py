import pytest
from app.models.user import User

@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": User.hash_password("testpassword")
    }

def test_hash_password():
    password = "testpassword"
    hashed = User.hash_password(password)
    assert hashed != password
    assert User.verify_password(password) == True

    user = User(username="testuser", email="testuser@example.com", password_hash=hashed)
    assert user.verify_password("testpassword") == True

def test_verify_password(user_data):
    user = User(**user_data)
    assert user.verify_password("testpassword") == True
    assert user.verify_password("wrongpassword") == False

def test_user_repr(user_data):
    user = User(**user_data)
    repr_str = repr(user)
    assert "username=testuser" in repr_str
    assert "email=testuser@example.com" in repr_str

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

User.metadata.create_all(bind=engine)

def test_create_user_in_db():
    session = SessionLocal()
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password_hash": User.hash_password("testpassword")
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    db_user = session.query(User).filter_by(username="testuser").first()
    assert db_user is not None
    assert db_user.verify_password("testpassword") == True

    session.close()

def test_invalid_password_in_db():
    session = SessionLocal()
    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password_hash": User.hash_password("correctpassword")
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    db_user = session.query(User).filter_by(username="testuser2").first()
    assert db_user is not None
    assert db_user.verify_password("incorrectpassword") == False

    session.close()
