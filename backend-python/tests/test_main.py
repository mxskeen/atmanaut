"""
Basic tests for the FastAPI backend
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Atmanaut FastAPI Backend"
    assert data["status"] == "running"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "atmanaut-backend"

def test_daily_prompt():
    """Test public daily prompt endpoint"""
    response = client.get("/api/v1/public/daily-prompt")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data

def test_protected_endpoint_without_auth():
    """Test that protected endpoints require authentication"""
    response = client.get("/api/v1/collections/")
    assert response.status_code == 401

def test_api_documentation():
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/openapi.json")
    assert response.status_code == 200
