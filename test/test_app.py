import os
import sys
import pytest
import json

from dao import user
from app import app, init_db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()  # Initialize the database for testing
        user.remove_test_data("testuser")
        yield client


def test_create_account_success(client):
    """Test account creation with valid input"""
    response = client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['success'] is True


def test_create_account_username_exists(client):
    """Test account creation when username already exists"""
    client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')

    response = client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] is False
    assert data['reason'] == "Username already exists"


def test_create_account_invalid_username(client):
    """Test account creation with invalid username"""
    response = client.post('/create_account', data=json.dumps({
        "username": "tu",
        "password": "Password123"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] is False
    assert data['reason'] == "Username must be between 3 and 32 characters"


def test_create_account_invalid_password(client):
    """Test account creation with invalid password"""
    response = client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "pwd"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] is False
    assert data['reason'] == "Password must be between 8 and 32 characters, contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"


def test_verify_account_success(client):
    """Test account verification with valid username and password"""
    client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')

    response = client.post('/verify_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] is True


def test_verify_account_invalid_password(client):
    """Test account verification with invalid password"""
    client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')

    response = client.post('/verify_account', data=json.dumps({
        "username": "testuser",
        "password": "WrongPassword"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['success'] is False
    assert data['reason'] == "Invalid username or password"


def test_verify_account_rate_limit(client):
    """Test account verification rate limiting after 5 failed attempts"""
    client.post('/create_account', data=json.dumps({
        "username": "testuser",
        "password": "Password123"
    }), content_type='application/json')

    for _ in range(5):
        client.post('/verify_account', data=json.dumps({
            "username": "testuser",
            "password": "WrongPassword"
        }), content_type='application/json')

    response = client.post('/verify_account', data=json.dumps({
        "username": "testuser",
        "password": "WrongPassword"
    }), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] is False
    assert data['reason'] == "Too many failed attempts. Please wait one minute before trying again."
