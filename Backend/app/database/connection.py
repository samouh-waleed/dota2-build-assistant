from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Fetch database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL: # If the URL is not found rais an error
    raise ValueError("No DATABASE_URL environment variable found")

# Create the engine, which is the core interface to the database
engine = create_engine(DATABASE_URL)

# sessionLocal is a factory that creates new sessions for each request, bound to the engine 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class that our model will inherit from
Base = declarative_base()