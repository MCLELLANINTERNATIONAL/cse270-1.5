import requests

# Base URL for the users endpoint
BASE_URL = "http://127.0.0.1:8000/users/"


def test_valid_user_returns_200():
    """
    Test 1:
    Send a GET request with valid credentials.
    Verify that the response status code is 200.
    """

    # Define query parameters for valid login
    params = {
        "username": "admin",
        "password": "qwerty"
    }

    # Send GET request to the endpoint
    response = requests.get(BASE_URL, params=params)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


def test_invalid_user_returns_401():
    """
    Test 2:
    Send a GET request with invalid credentials.
    Verify that the response status code is 401.
    """

    # Define query parameters for invalid login
    params = {
        "username": "admin",
        "password": "admin"
    }

    # Send GET request to the endpoint
    response = requests.get(BASE_URL, params=params)

    # Assert that the response status code is 401 (Unauthorized)
    assert response.status_code == 401