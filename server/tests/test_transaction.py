from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Transaction


@pytest.mark.asyncio
async def test_create_transaction(async_client: AsyncClient, async_session: AsyncSession) -> None:
    # Test data
    transaction_data = {
        "method": "GET",
        "path": "/api/v1/test",
        "status": 200,
        "process_time": 0.1234,
        "client_host": "127.0.0.1",
        "forwarded_for": None,
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Make request
    response = await async_client.post("/transactions", json=transaction_data)

    assert response.status_code == 201
    data = response.json()

    # Check response data
    assert data["method"] == transaction_data["method"]
    assert data["path"] == transaction_data["path"]
    assert data["status"] == transaction_data["status"]
    assert data["process_time"] == transaction_data["process_time"]
    assert data["client_host"] == transaction_data["client_host"]
    assert data["forwarded_for"] == transaction_data["forwarded_for"]
    assert "id" in data
    assert "logged_at" in data

    # Verify database entry
    db_transaction = await async_session.get(Transaction, data["id"])
    assert db_transaction is not None
    assert db_transaction.method == transaction_data["method"]
    assert db_transaction.path == transaction_data["path"]


@pytest.mark.asyncio
async def test_create_transaction_invalid_data(async_client: AsyncClient, async_session: AsyncSession) -> None:
    # Missing required fields
    invalid_data = {
        "method": "GET",
        "path": "/api/v1/test",
        # missing other required fields
    }

    response = await async_client.post("/transactions", json=invalid_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_transaction_with_forwarded_for(async_client: AsyncClient, async_session: AsyncSession) -> None:
    transaction_data = {
        "method": "POST",
        "path": "/api/v1/test",
        "status": 201,
        "process_time": 0.5678,
        "client_host": "127.0.0.1",
        "forwarded_for": "10.0.0.1",
        "timestamp": datetime.utcnow().isoformat(),
    }

    response = await async_client.post("/transactions", json=transaction_data)
    assert response.status_code == 201
    data = response.json()
    assert data["forwarded_for"] == "10.0.0.1"
