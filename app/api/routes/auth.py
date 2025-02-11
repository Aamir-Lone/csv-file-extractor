from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text  # Import text() for raw SQL queries
from app.db.database import get_db
from app.db.models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.db.database import get_db
from app.workers.tasks import scrape_metadata  # Import scrape_metadata task

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT (use a strong, randomly generated one)
SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ✅ Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ✅ Password hashing functions
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Token generation
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Register a new user
# @router.post("/register")
# async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
#     result = await db.execute(query, {"email": user.email})
#     user_exists = result.fetchone()
@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)): 
    query = select(User).where(User.email == user.email)
    result = await db.execute(query)  
    user_exists = result.fetchone()
    
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()  # Commit the changes
    await db.refresh(new_user)  # Refresh the object with updated data

    return {"message": "User registered successfully"}


# ✅ User Login
@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
    result = await db.execute(query, {"email": user.email})
    existing_user = result.fetchone()
    
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": existing_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Verify JWT Token & Get Current User
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
        result = await db.execute(query, {"email": email})
        user = result.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ Example of a protected route
@router.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello, {user.username}. You are authenticated!"}


router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT (use a strong, randomly generated one)
SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ✅ Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ✅ Password hashing functions
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Token generation
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Register a new user
@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
    result = await db.execute(query, {"email": user.email})
    user_exists = result.fetchone()
    
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()  # Use async commit for AsyncSession
    await db.refresh(new_user)  # Use async refresh for AsyncSession

    return {"message": "User registered successfully"}


# ✅ User Login
@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
    result = await db.execute(query, {"email": user.email})
    existing_user = result.fetchone()
    
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": existing_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Verify JWT Token & Get Current User
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
        result = await db.execute(query, {"email": email})
        user = result.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ Example of a protected route
@router.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello, {user.username}. You are authenticated!"}
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text  # Import text() for raw SQL queries
from app.db.database import get_db
# from app.db.user_model import User
from app.db.models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT (use a strong, randomly generated one)
SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ✅ Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ✅ Password hashing functions
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Token generation
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Register a new user
@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
    result = await db.execute(query, {"email": user.email})
    user_exists = result.fetchone()
    
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()  # Use async commit for AsyncSession
    await db.refresh(new_user)  # Use async refresh for AsyncSession

    return {"message": "User registered successfully"}


# ✅ User Login
@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
    result = await db.execute(query, {"email": user.email})
    existing_user = result.fetchone()
    
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": existing_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Verify JWT Token & Get Current User
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        query = text("SELECT * FROM users WHERE email = :email")  # Use text() for raw SQL query
        result = await db.execute(query, {"email": email})
        user = result.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ Example of a protected route
@router.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello, {user.username}. You are authenticated!"}


# The endpoint for uploading CSV and starting the scraping task
@router.post("/upload")
async def upload_csv(file: UploadFile, db: AsyncSession = Depends(get_db)):
    # Parse the CSV file (for simplicity, assuming each line in the CSV is a URL)
    csv_data = await file.read()
    decoded_data = csv_data.decode("utf-8").splitlines()

    for row in decoded_data:
        url = row.strip()  # Remove any extra spaces/newlines around the URL
        # Trigger Celery task to scrape the metadata for each URL
        scrape_metadata.apply_async(args=[url, db])  # Enqueue the task in Celery

    return {"message": "CSV uploaded and scraping started!"}

