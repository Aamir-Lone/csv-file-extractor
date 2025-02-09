# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/test")
# def test_upload():
#     return {"message": "Upload route is working"}
# import csv
# import io
# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.db.models import URLRecord  # Assuming a model to store URLs

# router = APIRouter()

# @router.post("/upload")
# async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if not file.filename.endswith(".csv"):
#         raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

#     content = await file.read()
#     decoded_content = content.decode("utf-8")
#     csv_reader = csv.reader(io.StringIO(decoded_content))
    
#     urls = []
#     for row in csv_reader:
#         if row:  # Ensure the row is not empty
#             url = row[0].strip()
#             if url.startswith("http"):  # Basic URL validation
#                 urls.append(url)
    
#     if not urls:
#         raise HTTPException(status_code=400, detail="No valid URLs found in the file.")
    
#     # Save URLs to the database
#     for url in urls:
#         db.add(URLRecord(url=url, status="pending"))
#     db.commit()
    
#     return {"message": f"{len(urls)} URLs uploaded successfully", "uploaded_urls": urls}
# *************************************************************************************************

from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
import csv
from app.db.database import get_db
from app.db.models import URLRecord

router = APIRouter()

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
