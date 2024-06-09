import pytest
from starlette import status
from fastapi.testclient import TestClient

from src.main import app
from src.user.models import SexEnum, RoleEnum


client = TestClient(app)


@pytest.mark.asyncio
async def test_create_user():
    payload = dict(
        username="testuser",
        email="testuser@test.com",
        password="testpassword",
        sex=SexEnum.MALE,
        role=RoleEnum.USER,
        created_by=None
    )

    response = client.post("/user/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@test.com"
    assert "password" not in data


@pytest.mark.asyncio
async def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Hello Guys!"


@pytest.mark.asyncio
async def test_nonexistent_endpoint():
    response = client.get("/nonexistent_endpoint")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_protected_endpoint_without_token():
    response = client.get("/user/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
