# getenv() function is part of Python's built-in os module.
# But because we used a .env file to fake the environment variable,
# we need to first call load_dotenv() from the python-dotenv module.
# In production, DB_URL will be a proper environment variable.
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Connect to the database using the env variable
# Manages the overall connection
engine = create_engine(getenv("DB_URL"), echo=True, pool_size=20, max_overflow=0)
# Creates temp connections for CRUD
Session = sessionmaker(bind=engine)
# Maps the models to real MySQL tables
Base = declarative_base()
