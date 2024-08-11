from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import create_user as create_user_crud, get_users, get_user, delete_user as delete_user_crud , add_dummy_data, update_user as update_user_crud
from app.models.user import User  # Directly import the User model
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate  # Directly import the UserCreate and UserResponse schemas
from app.database import engine, SessionLocal

# Create the tables in the database based on the models, if they don't exist
User.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Event handler that runs when the application starts up
@app.on_event("startup")

def startup_event():

    db = SessionLocal()  # Create a session
    add_dummy_data(db)  # Add dummy data to the database
    db.close()  # Close the session

# Route to create a new user
@app.post("/users/", response_model=UserResponse)

def create_user(user: UserCreate, db: Session = Depends(get_db)):

    return create_user_crud(db=db, user=user)  # Call the CRUD function to create a user

# Route to retrieve a list of users
@app.get("/users/", response_model=list[UserResponse])

def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    return get_users(db, skip=skip, limit=limit)  # Call the CRUD function to get users

# Route to retrieve a single user by their ID
@app.get("/users/{user_id}", response_model=UserResponse)

def read_user(user_id: str, db: Session = Depends(get_db)):

    db_user = get_user(db, user_id=user_id)  # Call the CRUD function to get a user

    if db_user is None:  # If the user doesn't exist, raise a 404 error

        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user  # Return the user data

# Route to update a user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):

    return update_user_crud(db=db, user_id=user_id, user_update=user_update)

# Route to delete a user
@app.delete("/users/{user_id}", response_model=UserResponse)

def delete_user(user_id: str, db: Session = Depends(get_db)):

    return delete_user_crud(db=db, user_id=user_id)