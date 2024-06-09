import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.user.models import SexEnum, RoleEnum
from src.user.schemas import UserCreate


client = TestClient(app)


@pytest.mark.asyncio
async def test_create_user():
    test_user = UserCreate(
        username="testuser",
        email="testuser@test.com",
        password="testpassword",
        sex=SexEnum.MALE,
        role=RoleEnum.USER,
        created_by=None
    )
    response = client.post("/users/", json=test_user.dict())
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@test.com"
    assert "password" not in data
