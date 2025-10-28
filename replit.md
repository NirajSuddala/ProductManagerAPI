# Product Management API with Replit Auth

## Overview
A complete FastAPI backend application for product management with PostgreSQL database integration and Replit Auth for secure user authentication. The project uses SQLAlchemy for ORM, Pydantic for data validation, and provides full CRUD (Create, Read, Update, Delete) operations for managing products.

**Created:** October 27, 2025  
**Last Updated:** October 28, 2025 - Added Replit Auth

## Project Architecture

### File Structure
```
.
├── main.py          # FastAPI application with endpoints, lifespan, and session middleware
├── database.py      # SQLAlchemy engine, session maker, and dependency
├── models.py        # SQLAlchemy ORM models (User, Product)
├── schemas.py       # Pydantic models for validation
├── crud.py          # CRUD operations and sample data
├── replit_auth.py   # Replit Auth OAuth configuration and helpers
├── auth_routes.py   # Authentication endpoints (login, callback, logout)
├── requirements.txt # Python dependencies
└── .gitignore      # Python-specific gitignore
```

### Technology Stack
- **Framework:** FastAPI 0.109.0
- **Server:** Uvicorn 0.27.0
- **ORM:** SQLAlchemy 2.0.25
- **Database:** PostgreSQL (via psycopg2-binary 2.9.9)
- **Validation:** Pydantic 2.5.3
- **Authentication:** Replit Auth (OpenID Connect via Authlib 1.6.5)
- **Session Management:** Starlette Sessions with itsdangerous 2.2.0
- **Configuration:** python-dotenv 1.0.0

## Features

### Authentication
The application uses **Replit Auth** for secure user authentication via OpenID Connect (OIDC). Users can log in with:
- Google
- GitHub
- X (Twitter)
- Apple
- Email/Password

Authentication endpoints:
- `GET /auth/login` - Redirects to Replit OAuth login
- `GET /auth/callback` - OAuth callback handler (validates ID token)
- `GET /auth/logout` - Logs out user and ends session
- `GET /auth/me` - Returns current user information

### API Endpoints
- `GET /` - Welcome message (shows auth status and user info if logged in)
- `GET /products/` - List all products (with pagination) - **Public**
- `GET /products/{product_id}` - Get a single product by ID - **Public**
- `POST /products/` - Create a new product - **Requires Authentication**
- `PATCH /products/{product_id}` - Update a product - **Requires Authentication**
- `DELETE /products/{product_id}` - Delete a product - **Requires Authentication**

### Database Initialization
The application automatically creates database tables and populates them with 4 sample products on startup:
1. Rose Gold Samantha Pendant Necklace (Jewelry)
2. Radiance Katrina Glow Serum (Beauty)
3. Diamond Stud Earrings (Jewelry)
4. Velvet Matte Lipstick (Beauty)

### User Schema
Each authenticated user contains:
- `id` (String) - Unique identifier from Replit (sub claim)
- `email` (String, nullable) - User email
- `first_name` (String, nullable) - User first name
- `last_name` (String, nullable) - User last name
- `profile_image_url` (String, nullable) - Profile image URL
- `created_at` (DateTime) - Account creation timestamp
- `updated_at` (DateTime) - Last update timestamp

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

The application uses the following environment variables:
- `DATABASE_URL` - PostgreSQL database connection string (automatically configured)
- `REPL_ID` - Replit project ID (automatically available, used as OAuth client_id)
- `SESSION_SECRET` - Secret key for session encryption (automatically configured)
- `ISSUER_URL` - OAuth issuer URL (defaults to https://replit.com/oidc)

## Security

The application implements secure authentication with proper validation:
- ID token signature verification using Replit's JWKS
- Issuer, audience, expiration, and nonce validation
- Secure session management with encrypted cookies
- Protected routes require valid authentication
- OAuth 2.0 with PKCE for secure authorization flow

## Recent Changes

**October 28, 2025** - Added Replit Auth
- Integrated Replit Auth (OpenID Connect) for user authentication
- Updated User model to support OAuth user data (id, email, profile info)
- Created replit_auth.py with OAuth configuration and helper functions
- Implemented authentication routes (login, callback, logout, me)
- Added session middleware for secure session management
- Protected product creation, update, and delete routes
- Implemented proper ID token validation with signature verification
- Removed old username/password authentication system

**October 27, 2025** - Initial project setup
- Created modular FastAPI application structure
- Implemented SQLAlchemy ORM with Product model
- Added Pydantic schemas for data validation
- Implemented complete CRUD operations
- Set up automatic database initialization with sample data
- Configured FastAPI lifespan for startup tasks
- Successfully tested all CRUD endpoints
