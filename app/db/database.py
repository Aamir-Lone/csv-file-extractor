
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv
# from sqlalchemy.ext.declarative import declarative_base
# from app.db.models import Base

# # Load environment variables
# load_dotenv()


# DATABASE_URL = "postgresql+asyncpg://postgres:Aamirlone@localhost:5432/web_scraper"


# # Create async engine
# engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Base = declarative_base()

# # Create session
# AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
# def init_db():
#     # This function can be used to create the tables if they don't exist
#     Base.metadata.create_all(bind=engine)

# # Dependency for DB session
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session
# **********************************************************************************
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# DATABASE_URL = "postgresql+asyncpg://postgres:Aamirlone@localhost:5432/web_scraper"
DATABASE_URL= s.getenv("DATABASE_URL")

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)

# Define the base class for models
Base = declarative_base()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+asyncpg://postgres:Aamirlone@localhost:5432/web_scraper"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

def init_db():
    """Initializes the database by creating all tables."""
    from app.db.models import Base  # Import inside function to avoid circular imports
    Base.metadata.create_all(bind=engine)


# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
# Import models at the end to avoid circular imports
from app.db import models  # Import all models so Alembic detects them
