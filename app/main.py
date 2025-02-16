from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, upload, status, results
from app.db.database import init_db
import asyncio
from app.api.routes import upload
from app.workers.celery import celery 

# app = FastAPI()
app = FastAPI(title="Web Scraper API", version="1.0")

@app.on_event("startup")
async def startup_event():
    await init_db()


# Create FastAPI instance


# CORS Middleware (Allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(status.router, prefix="/status", tags=["Scraping Status"])
app.include_router(results.router, prefix="/results", tags=["Results"])
app.include_router(upload.router, prefix="/csv", tags=["CSV"])
# Include your API router (auth in this case) for routes like registration, login, etc.
app.include_router(auth.router)


# This ensures the Celery worker is ready to process tasks
celery.start(argv=['worker', '--loglevel=info'])  # Start Celery Worker


# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Web Scraper API"}

