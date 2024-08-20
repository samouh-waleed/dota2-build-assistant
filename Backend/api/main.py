from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router  
from app.database.connection import engine, Base

app = FastAPI()

# CORS settings
origins = [
    "http://localhost:3000",
    # Add other origins as necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Include the API routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dota 2 Build Assistant API"}
