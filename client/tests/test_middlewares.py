from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from openapm.middlewares import FastAPIMiddleware


@pytest.fixture
def mock_endpoint():
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        yield "http://test-endpoint:8000"


@pytest.fixture
def app(mock_endpoint):
    app = FastAPI()
    app.add_middleware(FastAPIMiddleware, endpoint=mock_endpoint)

    @app.get("/test")
    def test_route():
        return {"message": "test"}

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_middleware_initialization():
    with patch("requests.get") as mock_get:
        # Test successful initialization
        mock_get.return_value = Mock(status_code=200)
        app = FastAPI()
        middleware = FastAPIMiddleware(app, "http://valid-endpoint:8000")
        assert middleware.endpoint == "http://valid-endpoint:8000"

        # Test failed initialization
        mock_get.return_value = Mock(status_code=404)
        with pytest.raises(ValueError, match="Unable to reach endpoint"):
            FastAPIMiddleware(app, "http://invalid-endpoint:8000")


def test_middleware_request_handling(client, mock_endpoint):
    with patch("requests.post") as mock_post:
        response = client.get("/test")
        assert response.status_code == 200
        assert response.json() == {"message": "test"}

        # Verify the background task was created
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Check the endpoint
        assert call_args[0][0] == "http://test-endpoint:8000/transactions"

        # Check the payload structure
        payload = call_args[1]["json"]
        assert set(payload.keys()) == {
            "timestamp",
            "method",
            "path",
            "status",
            "process_time",
            "client_host",
            "forwarded_for",
        }
        assert payload["method"] == "GET"
        assert payload["path"] == "/test"
        assert payload["status"] == 200
        assert isinstance(payload["process_time"], float)
