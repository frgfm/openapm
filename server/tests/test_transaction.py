from datetime import datetime

import pytest
from fastapi import status
from httpx import AsyncClient

from app.crud import TransactionCRUD
from app.main import app
from app.models import Transaction

# Mock data
VALID_TRANSACTION = {
    "method": "GET",
    "path": "/api/test",
    "status": 200,
    "process_time": 0.1234,
    "client_host": "127.0.0.1",
    "forwarded_for": None,
    "timestamp": datetime.utcnow().isoformat(),
}


@pytest.mark.asyncio
async def test_create_transaction_success(mocker):
    # Mock the database session and CRUD
    async def mock_create(self, payload):
        return Transaction(**payload.model_dump(), id=1)

    mocker.patch.object(TransactionCRUD, "create", mock_create)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/transaction", json=VALID_TRANSACTION)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["method"] == VALID_TRANSACTION["method"]
    assert data["path"] == VALID_TRANSACTION["path"]
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_create_transaction_invalid_data():
    invalid_data = VALID_TRANSACTION.copy()
    del invalid_data["method"]  # Remove required field

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/transaction", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_transaction_db_error(mocker):
    # Mock database error
    async def mock_create_error(self, payload):
        raise Exception("Database error")

    mocker.patch.object(TransactionCRUD, "create", mock_create_error)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/transaction", json=VALID_TRANSACTION)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
