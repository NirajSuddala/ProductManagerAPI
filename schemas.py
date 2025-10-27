from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    rating: int
    category: str
    ageRange: str
    description: str
    material: str
    inStock: bool
    image: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    rating: int | None = None
    category: str | None = None
    ageRange: str | None = None
    description: str | None = None
    material: str | None = None
    inStock: bool | None = None
    image: str | None = None

class Product(ProductBase):
    id: str

    class Config:
        from_attributes = True
