# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# import datetime
# from app.db.database import Base

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)



# # class ScrapedData(Base):
# #     __tablename__ = "scraped_data"

# #     id = Column(Integer, primary_key=True, index=True)
# #     url = Column(String, unique=True, nullable=False)
# #     title = Column(String, nullable=True)
# #     description = Column(String, nullable=True)
# #     keywords = Column(String, nullable=True)
# #     created_at = Column(DateTime, default=datetime.datetime.utcnow)
# app/db/models.py

# ***************************************************
from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base
from sqlalchemy.ext.declarative import declarative_base
# import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class URLRecord(Base):
    __tablename__ = "url_records"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    status = Column(String, default="pending")  # pending, in-progress, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Now this works!


class Metadata(Base):
    __tablename__ = "metadata"  # Ensure this matches your DB table name

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Now this works!
