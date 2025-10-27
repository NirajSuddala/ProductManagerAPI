from sqlalchemy import Column, String, Float, Integer, Boolean
from database import Base

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
