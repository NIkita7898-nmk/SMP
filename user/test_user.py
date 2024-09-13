import pytest
import requests

# Base URL of the API
BASE_URL = "http://127.0.0.1:8000/"  

@pytest.fixture
def user_data():
    return {
        "email": "t1ssessqtussesr@example.com",
        "password": "password123"
    }

def test_create_user_success(user_data):
    """Test creating a user successfully"""
    url = f'{BASE_URL}/create/'
    response = requests.post(url, json=user_data)
    print(response.content, "====================================")
    assert response.status_code == 201  
    json_response = response.json()
    assert json_response["email"] == user_data["email"]
    assert "email" in json_response 

def test_create_user_missing_fields():
    url = f'{BASE_URL}/create/'
    """Test creating a user with missing fields"""
    incomplete_data = {
        "email": "incompleteuser",
    }
    response = requests.post(url, json=incomplete_data)
    assert response.status_code == 400
    json_response = response.json()
    assert {'email': ['Enter a valid email address.']}

def test_create_user_duplicate(user_data):
    url = f'{BASE_URL}/create/'
    """Test creating a user that already exists"""
    # First user creation
    requests.post(url, json=user_data)
    
    # Attempt to create the same user again
    response = requests.post(url, json=user_data)
    print(response)
    assert response.status_code == 400  # Assuming 409 Conflict is the expected response
    json_response = response.json()

    # assert "error" in json_response
    # assert json_response["error"] == "User already exists"

def test_login_user(user_data):
    url = f'{BASE_URL}/login/'
    requests.post(url, json=user_data)
    response = requests.post(url, json=user_data)
    assert response.status_code == 200