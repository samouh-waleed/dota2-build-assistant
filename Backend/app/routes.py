from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers import user_controller
from app.schema import UserCreate, UserResponse, UserUpdate
from app.database_connection import engine, get_db
from app.models.user import User

# Initialize FastAPI
app = FastAPI()

# Create the tables in the database based on the models, if they don't exist
User.metadata.create_all(bind=engine)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Dota 2 Build Assistant API"}

# Route to create a new user
@app.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(user=user, db=db)

# Route to retrieve a list of users
@app.get("/users/", response_model=list[UserResponse])
def read_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_controller.get_users(skip=skip, limit=limit, db=db)

# Route to retrieve a single user by their ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user_route(user_id: str, db: Session = Depends(get_db)):
    return user_controller.get_user(user_id=user_id, db=db)

# Route to update a user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_route(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    return user_controller.update_user(user_id=user_id, user_update=user_update, db=db)

# Route to delete a user
@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user_route(user_id: str, db: Session = Depends(get_db)):
    return user_controller.delete_user(user_id=user_id, db=db)

# Optional: Add dummy data on startup- REMOVE THIS ONCE WE GET STEAM LOGING WOKRING
@app.on_event("startup")
def startup_event():
    db = next(get_db())  # Retrieve the session from the generator
    user_controller.add_dummy_data(db=db)
    db.close()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
