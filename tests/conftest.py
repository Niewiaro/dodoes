from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.model import TokenData
from src.auth.service import get_password_hash
from src.database.core import Base
from src.entities.todo import Todo, Priority
from src.entities.user import User
from src.rate_limiting import limiter


@pytest.fixture(scope="function")
def db_session(tmp_path):
    DB_PATH = tmp_path / "test.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user():
    # Create a user with a known password hash
    password_hash = get_password_hash("password123")
    return User(
        id=uuid4(),
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password_hash=password_hash
    )


@pytest.fixture(scope="function")
def test_token_data():
    return TokenData(user_id=str(uuid4()))


@pytest.fixture(scope="function")
def test_todo(test_token_data):
    return Todo(
        id=uuid4(),
        description="Test Description",
        user_id=test_token_data.get_uuid()
    )


@pytest.fixture(scope="function")
def test_todo_fill_all(test_token_data):
    return Todo(
        id=uuid4(),
        description="Test Description",
        user_id=test_token_data.get_uuid(),
        due_date=datetime.now(timezone.utc),
        starts_at=datetime.now(timezone.utc),
        is_completed=True,
        priority=Priority.Top,
        completed_at=datetime.now(timezone.utc),
    )


@pytest.fixture(scope="function")
def client(db_session):
    from src.main import app
    from src.database.core import get_db

    # Disable rate limiting for tests
    limiter.reset()

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    # Register a test user
    response = client.post(
        "/auth/register",
        json={
            "email": "test.user@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "grant_type": "password"
        }
    )
    assert response.status_code == 201

    # Login to get access token
    response = client.post(
        "/auth/login",
        data={
            "username": "test.user@example.com",
            "password": "testpassword123",
            "grant_type": "password"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
