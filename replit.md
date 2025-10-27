# Product Management API

## Overview
A complete FastAPI backend application for product management with PostgreSQL database integration. The project uses SQLAlchemy for ORM, Pydantic for data validation, and provides full CRUD (Create, Read, Update, Delete) operations for managing products.

**Created:** October 27, 2025

## Project Architecture

### File Structure
```
.
├── main.py          # FastAPI application with endpoints and lifespan
├── database.py      # SQLAlchemy engine, session maker, and dependency
├── models.py        # SQLAlchemy ORM Product model
├── schemas.py       # Pydantic models for validation
├── crud.py          # CRUD operations and sample data
├── requirements.txt # Python dependencies
└── .gitignore      # Python-specific gitignore
```

### Technology Stack
- **Framework:** FastAPI 0.109.0
- **Server:** Uvicorn 0.27.0
- **ORM:** SQLAlchemy 2.0.25
- **Database:** PostgreSQL (via psycopg2-binary 2.9.9)
- **Validation:** Pydantic 2.5.3
- **Configuration:** python-dotenv 1.0.0

## Features

### API Endpoints
- `GET /` - Welcome message
- `GET /products/` - List all products (with pagination)
- `GET /products/{product_id}` - Get a single product by ID
- `POST /products/` - Create a new product
- `PUT /products/{product_id}` - Update a product
- `DELETE /products/{product_id}` - Delete a product

### Database Initialization
The application automatically creates database tables and populates them with 4 sample products on startup:
1. Rose Gold Samantha Pendant Necklace (Jewelry)
2. Radiance Katrina Glow Serum (Beauty)
3. Diamond Stud Earrings (Jewelry)
4. Velvet Matte Lipstick (Beauty)

### Product Schema
Each product contains:
- `id` (String) - Unique identifier
- `name` (String) - Product name
- `price` (Float) - Product price
- `rating` (Integer) - Product rating (1-5)
- `category` (String) - Product category
- `ageRange` (String) - Target age range
- `description` (String) - Product description
- `material` (String) - Product material
- `inStock` (Boolean) - Stock availability
- `image` (String) - Image URL

## Running the Application

The FastAPI server runs automatically via the configured workflow:
- **Host:** 0.0.0.0
- **Port:** 5000
- **Auto-reload:** Enabled

Access the API at: `http://localhost:5000`
Interactive API documentation: `http://localhost:5000/docs`

## Environment Variables

The application uses the following environment variable:
- `DATABASE_URL` - PostgreSQL database connection string (automatically configured)

## Recent Changes

**October 27, 2025** - Initial project setup
- Created modular FastAPI application structure
- Implemented SQLAlchemy ORM with Product model
- Added Pydantic schemas for data validation
- Implemented complete CRUD operations
- Set up automatic database initialization with sample data
- Configured FastAPI lifespan for startup tasks
- Successfully tested all CRUD endpoints
