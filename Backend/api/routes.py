from fastapi import APIRouter, Depends, HTTPException  # Use APIRouter instead of FastAPI
from sqlalchemy.orm import Session
from app.controllers import user_controller
from app.models.schema import UserCreate, UserResponse, UserUpdate
from app.database.connection import engine, get_db
from app.models.user import User

router = APIRouter()

# Create the tables in the database based on the models, if they don't exist
User.metadata.create_all(bind=engine)

@router.get("/")
def read_root():
    return {"message": "Welcome to the Dota 2 Build Assistant API"}

@router.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(user=user, db=db)

@router.get("/users/", response_model=list[UserResponse])
def read_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_controller.get_users(skip=skip, limit=limit, db=db)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user_route(user_id: str, db: Session = Depends(get_db)):
    return user_controller.get_user(user_id=user_id, db=db)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_route(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    return user_controller.update_user(user_id=user_id, user_update=user_update, db=db)

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user_route(user_id: str, db: Session = Depends(get_db)):
    return user_controller.delete_user(user_id=user_id, db=db)
