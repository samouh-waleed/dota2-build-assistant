from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database_connection import Base

class User(Base):
    __tablename__ = "users"

    # Define the columns in the users table
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # The primary key column, UUID type
    email = Column(String, unique=True, index=True)  # Email column, must be unique, and indexed for faster lookups
    username = Column(String, unique=True, index=True)  # Username column, must be unique, and indexed for faster lookups