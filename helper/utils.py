# Authenticate user and assign new token if credentials are valid
import json
import uuid
from typing import Optional
from helper.models import User

# Path to the local JSON "database"
db_path = "./helper/db.json"

# Load the current state of the database from the JSON file
def load_db():
    try:
        with open(db_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return empty dict if db file doesn't exist

# Save updated state back to the JSON file
def save_db(data):
    with open(db_path, "w") as f:
        json.dump(data, f, indent=4)

# Authenticate user and assign new token if credentials are
def authenticate_user(username: str, password: str) -> Optional[str]:
    db = load_db()
    # Check if the user exists and password matches
    if username in db and db[username]["password"] == password:
        token = str(uuid.uuid4())  # Generate a new UUID token
        db[username]["token"] = token  # Save the token for that user
        save_db(db)  # Persist updated DB
        return token
    return None  # Return None if authentication fails

# Verifies if the provided token matches what's stored for the user
def verify_token(username: str, token: str) -> bool:
    db = load_db()
    return username in db and db[username].get("token") == token
