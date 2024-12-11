from datetime import datetime

import pytest

from app.crud import TransactionCRUD, TransactionPayload
from app.models import Transaction

VALID_PAYLOAD = TransactionPayload(
    method="GET",
    path="/api/test",
    status=200,
    process_time=0.1234,
    client_host="127.0.0.1",
    forwarded_for=None,
    timestamp=datetime.utcnow(),
)


@pytest.mark.asyncio
async def test_transaction_crud_create(async_session, mocker):
    crud = TransactionCRUD(async_session)

    # Mock session methods
    mocker.patch.object(async_session, "commit", return_value=mocker.AsyncMock()())
    mocker.patch.object(async_session, "refresh", return_value=None).return_value = None

    result = await crud.create(VALID_PAYLOAD)

    assert isinstance(result, Transaction)
    assert result.method == VALID_PAYLOAD.method
    assert result.path == VALID_PAYLOAD.path
    assert async_session.commit.called
    assert async_session.refresh.called


# @pytest.mark.asyncio
# async def test_transaction_crud_create_foreign_key_error(async_session, mocker):
#     crud = TransactionCRUD(async_session)

#     # Mock session methods to raise ForeignKeyViolationError
#     async def mock_commit():
#         raise IntegrityError(statement="", params={}, orig=ForeignKeyViolationError())

#     mocker.patch.object(async_session, "commit", mock_commit)
#     mocker.patch.object(async_session, "rollback", return_value=None).return_value = None

#     with pytest.raises(HTTPException) as exc_info:
#         await crud.create(VALID_PAYLOAD)

#     assert exc_info.value.status_code == 404
#     assert async_session.rollback.called


# @pytest.mark.asyncio
# async def test_transaction_crud_create_unique_violation(async_session, mocker):
#     crud = TransactionCRUD(async_session)

#     # Mock session methods to raise UniqueViolationError
#     async def mock_commit():
#         raise IntegrityError(statement="", params={}, orig=UniqueViolationError())

#     mocker.patch.object(async_session, "commit", mock_commit)
#     mocker.patch.object(async_session, "rollback", return_value=None).return_value = None

#     with pytest.raises(HTTPException) as exc_info:
#         await crud.create(VALID_PAYLOAD)

#     assert exc_info.value.status_code == 409
#     assert async_session.rollback.called


# @pytest.mark.asyncio
# async def test_transaction_crud_get(async_session, mocker):
#     crud = TransactionCRUD(async_session)
#     mock_transaction = Transaction(id=1, **VALID_PAYLOAD.model_dump())

#     mocker.patch.object(async_session, "get", return_value=mock_transaction)

#     result = await crud.get(1)
#     assert result == mock_transaction
#     async_session.get.assert_called_once_with(Transaction, 1)


# @pytest.mark.asyncio
# async def test_transaction_crud_get_not_found(async_session, mocker):
#     crud = TransactionCRUD(async_session)

#     mocker.patch.object(async_session, "get", return_value=None)

#     with pytest.raises(HTTPException) as exc_info:
#         await crud.get(1, strict=True)

#     assert exc_info.value.status_code == 404


# @pytest.mark.asyncio
# async def test_transaction_crud_fetch_all(async_session, mocker):
#     crud = TransactionCRUD(async_session)
#     mock_transactions = [
#         Transaction(id=1, **VALID_PAYLOAD.model_dump()),
#         Transaction(id=2, **VALID_PAYLOAD.model_dump()),
#     ]

#     # Mock the exec method to return our mock transactions
#     mock_exec = mocker.AsyncMock(return_value=mock_transactions)
#     mocker.patch.object(async_session, "exec", mock_exec)

#     results = await crud.fetch_all()
#     assert results == mock_transactions


# @pytest.mark.asyncio
# async def test_transaction_crud_delete(async_session, mocker):
#     crud = TransactionCRUD(async_session)
#     mock_transaction = Transaction(id=1, **VALID_PAYLOAD.model_dump())

#     # Mock get and exec methods
#     mocker.patch.object(crud, "get", return_value=mock_transaction)
#     mocker.patch.object(async_session, "exec", return_value=None).return_value = None
#     mocker.patch.object(async_session, "commit", return_value=None).return_value = None

#     await crud.delete(1)

#     assert async_session.exec.called
#     assert async_session.commit.called


# @pytest.mark.asyncio
# async def test_transaction_crud_delete_not_found(async_session, mocker):
#     crud = TransactionCRUD(async_session)

#     # Mock get to return None
#     mocker.patch.object(crud, "get", return_value=None)

#     with pytest.raises(HTTPException) as exc_info:
#         await crud.delete(1)

#     assert exc_info.value.status_code == 404
