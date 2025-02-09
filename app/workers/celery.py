from celery import Celery

# Setup for Celery
celery = Celery(
    "scraper",
    backend="redis://localhost:6379/0",  # Result Backend (optional)
    broker="redis://localhost:6379/0",   # Task Queue Broker
)
celery.conf.task_routes = {"tasks.scrape_metadata": "scraper_queue"}  # Optional routing
