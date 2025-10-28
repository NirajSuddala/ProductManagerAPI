from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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
