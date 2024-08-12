from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.schema import UserCreate, UserUpdate
from app.database_connection import get_db

# Function to get a single user by ID
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Function to get a list of users, with optional pagination
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

# Function to create a new user
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    db_user = User(email=user.email, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to update a user by ID
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_update.email:
        db_user.email = user_update.email
    
    if user_update.username:
        db_user.username = user_update.username

    db.commit()
    db.refresh(db_user)
    return db_user

# Function to delete a user by ID
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

# Function to add dummy data (optional)
def add_dummy_data(db: Session = Depends(get_db)):
    dummy_users = [
        {"email": "user1@example.com", "username": "user1"},
        {"email": "user2@example.com", "username": "user2"},
        {"email": "user3@example.com", "username": "user3"},
    ]

    for user_data in dummy_users:
        try:
            user_create = UserCreate(email=user_data["email"], username=user_data["username"])
            create_user(user=user_create, db=db)
        except HTTPException as e:
            if e.status_code == status.HTTP_400_BAD_REQUEST:
                print(f"User {user_data['email']} already exists, skipping.")
