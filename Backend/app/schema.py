from pydantic import BaseModel
from typing import Optional
import uuid

# Define the schema for creating a user
class UserCreate(BaseModel):
    email: str  # Email field must be a string
    username: str  # Username field must be a string

# Define the schema for the response after a user is created, including the ID
class UserResponse(UserCreate):
    id: uuid.UUID  # The ID field, which is a UUID

    # Enable ORM mode, allowing the schema to work with ORM objects
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None # Email is optional and defaults to None
    username: Optional[str] = None  # Username is optional and defaults to None