from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    ageRange = Column(String, nullable=False)
    description = Column(String, nullable=False)
    material = Column(String, nullable=False)
    inStock = Column(Boolean, default=True, nullable=False)
    image = Column(String, nullable=False)
