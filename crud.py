from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductUpdate

SAMPLE_PRODUCTS = [{
    "id":
    "1",
    "name":
    "Rose Gold Samantha Pendant Necklace",
    "price":
    89.99,
    "rating":
    5,
    "category":
    "Jewelry",
    "ageRange":
    "All Ages",
    "description":
    "Elegant rose gold pendant...",
    "material":
    "Rose Gold",
    "inStock":
    True,
    "image":
    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop"
}, {
    "id":
    "2",
    "name":
    "Radiance Katrina Glow Serum",
    "price":
    45.00,
    "rating":
    4,
    "category":
    "Beauty",
    "ageRange":
    "All Ages",
    "description":
    "Luxurious serum...",
    "material":
    "Organic",
    "inStock":
    True,
    "image":
    "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&h=500&fit=crop"
}, {
    "id":
    "3",
    "name":
    "Diamond Samyuktha Stud Earrings",
    "price":
    199.99,
    "rating":
    5,
    "category":
    "Jewelry",
    "ageRange":
    "All Ages",
    "description":
    "Classic diamond studs...",
    "material":
    "White Gold",
    "inStock":
    True,
    "image":
    "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&h=500&fit=crop"
}, {
    "id":
    "4",
    "name":
    "Velvet Matte Lipstick",
    "price":
    28.00,
    "rating":
    5,
    "category":
    "Beauty",
    "ageRange":
    "Teen/Young Adult",
    "description":
    "Long-lasting matte lipstick...",
    "material":
    "Vegan",
    "inStock":
    True,
    "image":
    "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500&h=500&fit=crop"
}]


def initialize_products(db: Session):
    existing_count = db.query(Product).count()
    if existing_count == 0:
        for product_data in SAMPLE_PRODUCTS:
            db_product = Product(**product_data)
            db.add(db_product)
        db.commit()


def create_product(db: Session, product: ProductCreate):
    existing_products = db.query(Product).all()

    if existing_products:
        max_id = max(int(p.id) for p in existing_products)
        new_id = str(max_id + 1)
    else:
        new_id = "1"

    db_product = Product(id=new_id, **product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: str, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: str):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
