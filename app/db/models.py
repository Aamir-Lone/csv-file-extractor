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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
