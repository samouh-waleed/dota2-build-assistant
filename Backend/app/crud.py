from sqlalchemy.orm import Session
from app.models.user import User  # Directly import the User model
from app.schemas.user_schema import UserCreate, UserUpdate  # Directly import the UserCreate schema
from fastapi import HTTPException, status

# Function to get a single user by ID
def get_user(db: Session, user_id: str):

    return db.query(User).filter(User.id == user_id).first()

# Function to get a list of users, with optional pagination
def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(User).offset(skip).limit(limit).all()

# Function to create a new user
def create_user(db: Session, user: UserCreate):
    # Check if a user with the same email or username already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing_user:
        # If the user already exists, raise an HTTP 400 error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    # If the user does not exist, create a new user
    db_user = User(email=user.email, username=user.username)
    db.add(db_user)  # Add the user to the session
    db.commit()  # Commit the transaction, saving the user to the database
    db.refresh(db_user)  # Refresh the instance with the new data from the database
    return db_user  # Return the newly created user

# Function to update a user by ID
def update_user(db: Session, user_id: str, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:  # If the user doesn't exist, raise a 404 error
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.email:
        db_user.email = user_update.email
    
    if user_update.username:
        db_user.username = user_update.username

    db.commit()  # Commit the transaction, saving the changes to the database
    db.refresh(db_user)  # Refresh the instance with the new data from the database
    
    return db_user

# Function to delete a user by ID
def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:  # If the user doesn't exist, raise a 404 error
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)

    db.commit()  # Commit the transaction, saving the changes to the database

    return {"message": "User deleted"}

def add_dummy_data(db: Session):
    # List of dummy users to be added
    dummy_users = [
        {"email": "user1@example.com", "username": "user1"},
        {"email": "user2@example.com", "username": "user2"},
        {"email": "user3@example.com", "username": "user3"},
    ]

    for user_data in dummy_users:
        try:
            # Use the existing create_user function to add dummy data
            user_create = UserCreate(email=user_data["email"], username=user_data["username"])

            create_user(db=db, user=user_create)

        except HTTPException as e:

            if e.status_code == status.HTTP_400_BAD_REQUEST:

                print(f"User {user_data['email']} already exists, skipping.")

