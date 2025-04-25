import requests

BASE = "http://127.0.0.1:8000"

# Register a user
resp = requests.post(f"{BASE}/user/register", json={"username": "arky", "password": "lets_do_this"})
print(resp.json())

# Login and get token
resp = requests.post(f"{BASE}/auth/login", json={"username": "arky", "password": "lets_do_this"})
token = resp.json().get("token")
print("Token:", token)

# Access protected endpoint using the token
headers = {"token": token}
resp = requests.get(f"{BASE}/transcriber/data", params={"username": "arky"}, headers=headers)
print(resp.json())
