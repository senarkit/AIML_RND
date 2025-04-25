import requests
from fastapi import HTTPException

BASE_URL = "http://127.0.0.1:8000"

def sign_up():
    url = f"{BASE_URL}/auth/"
    payload = {
        "username": "test_user",
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123",
        "role": "user",
        "phone_number": "1234567890"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print("User created successfully!")
    else:
        print(f"Error: {response.status_code} - {response.json()}")

def login():
    url = f"{BASE_URL}/auth/token"
    payload = {
        "username": "test_user",
        "password": "password123"
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"Login successful. Access token: {token}")
        return token
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return None

def update_password(token):
    url = f"{BASE_URL}/user/password"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "password": "password123",
        "new_password": "new_password123"
    }

    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 204:
        print("Password updated successfully!")
    else:
        print(f"Error: {response.status_code} - {response.json()}")

def update_phone_number(token):
    url = f"{BASE_URL}/user/phonenumber/0987654321"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print("Phone number updated successfully!")
    else:
        print(f"Error: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    # Sign up a user
    sign_up()

    # Log in to get the token
    token = login()

    if token:
        # Use the token to update the password
        update_password(token)

        # Use the token to update the phone number
        update_phone_number(token)
