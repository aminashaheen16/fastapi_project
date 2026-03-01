import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy ✅"}

def test_root_endpoint():
    """Test the root endpoint message."""
    response = client.get("/api/")
    assert response.status_code == 200
    assert "FastAPI LLM API" in response.json()["message"]

def test_auth_me_without_token():
    """Test protected route without auth token should fail."""
    response = client.get("/api/auth/me")
    # Should return 403 Forbidden because no Bearer token is provided
    assert response.status_code == 403
