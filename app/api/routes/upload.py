from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
import csv
from app.db.database import get_db
from app.db.models import URLRecord

router = APIRouter()  # ✅ Define the router

@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        decoded_content = contents.decode("utf-8").splitlines()
        reader = csv.reader(decoded_content)

        for row in reader:
            url = row[0].strip()
            if url:  
                existing = db.query(URLRecord).filter(URLRecord.url == url).first()
                if not existing:
                    new_record = URLRecord(url=url)
                    db.add(new_record)
        
        db.commit()
        return {"message": "CSV uploaded successfully!"}
    except Exception as e:
        return {"error": str(e)}
