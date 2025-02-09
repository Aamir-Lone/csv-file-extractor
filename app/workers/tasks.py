import requests
from bs4 import BeautifulSoup
from celery import Celery
from app.db.models import Metadata  # Assuming you have a Metadata table for scraped data
from app.db.database import get_db  # The function for getting DB session
from app.workers.celery import celery

# Import Celery app
from .celery import celery

# Scrape metadata from a URL
@celery.task
def scrape_metadata(url, db_session):
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad responses

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract metadata (e.g., title, description, and keywords)
        title = soup.find("title").text if soup.find("title") else "No title"
        description = soup.find("meta", attrs={"name": "description"})
        description = description["content"] if description else "No description"
        keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords["content"] if keywords else "No keywords"

        # Store the metadata in the database (use your SQLAlchemy model)
        metadata = Metadata(
            url=url,
            title=title,
            description=description,
            keywords=keywords
        )
        
        # Commit data to the database
        db_session.add(metadata)
        db_session.commit()

        return {"status": "success", "url": url}
    
    except Exception as e:
        return {"status": "failed", "error": str(e)}
