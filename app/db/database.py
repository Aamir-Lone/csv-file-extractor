
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
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")  

# Ensure DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("⚠️ DATABASE_URL is not set. Please check your .env file.")

# Create Async SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)  

# Create async session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Base class for models
Base = declarative_base()

# Function to get a database session
async def get_db():
    """Dependency for FastAPI routes to get a database session."""
    async with SessionLocal() as session:
        yield session

# No more `Base.metadata.create_all()`
async def init_db():
    """Database initialization - Now handled via Alembic migrations."""
    pass
