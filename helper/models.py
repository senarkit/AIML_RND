from pydantic import BaseModel

# User model defines the data structure used for requests and internal operations
class User(BaseModel):
    username: str
    password: str
    token: str = ""  # Token is optional and defaults to empty
