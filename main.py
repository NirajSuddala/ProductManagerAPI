from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import engine, get_db, Base
from models import Product as ProductModel, User
from schemas import Product, ProductCreate, ProductUpdate
import crud
import auth_routes
from replit_auth import SESSION_SECRET, get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    db = next(get_db())
    try:
        crud.initialize_products(db)
    finally:
        db.close()
    
    yield

app = FastAPI(title="Product Management API", lifespan=lifespan)

# Add session middleware (must be added before routes)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth_routes.router)

@app.get("/")
async def read_root(request: Request, user: Optional[User] = Depends(get_current_user)):
    if user:
        return {
            "message": "Welcome to Product Management API",
            "authenticated": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
    return {
        "message": "Welcome to Product Management API",
        "authenticated": False,
        "login_url": "/auth/login"
    }

@app.post("/products/", response_model=Product)
async def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: str, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.patch("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: str, 
    product: ProductUpdate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    db_product = crud.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
async def delete_product(
    product_id: str, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    success = crud.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
