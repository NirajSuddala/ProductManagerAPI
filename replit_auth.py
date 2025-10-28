import os
import secrets
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from models import User
from database import get_db

REPL_ID = os.environ.get("REPL_ID")
ISSUER_URL = os.environ.get("ISSUER_URL", "https://replit.com/oidc")
SESSION_SECRET = os.environ.get("SESSION_SECRET")

if not REPL_ID:
    raise SystemExit("REPL_ID environment variable must be set")

if not SESSION_SECRET:
    SESSION_SECRET = secrets.token_urlsafe(32)

oauth = OAuth()
oauth.register(
    name='replit',
    client_id=REPL_ID,
    client_secret=None,
    server_metadata_url=f'{ISSUER_URL}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
        'code_challenge_method': 'S256',
    }
)


def get_current_user_from_session(request: Request, db: Session) -> Optional[User]:
    """Get the current user from session"""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user


def save_or_update_user(db: Session, user_claims: dict) -> User:
    """Save or update user from ID token claims"""
    user_id = str(user_claims.get('sub'))
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.email = user_claims.get('email')
        user.first_name = user_claims.get('first_name')
        user.last_name = user_claims.get('last_name')
        user.profile_image_url = user_claims.get('profile_image_url')
        user.updated_at = datetime.utcnow()
    else:
        user = User(
            id=user_id,
            email=user_claims.get('email'),
            first_name=user_claims.get('first_name'),
            last_name=user_claims.get('last_name'),
            profile_image_url=user_claims.get('profile_image_url')
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user


async def get_current_user(request: Request, db: Session = next(get_db())) -> Optional[User]:
    """Dependency to get current user (doesn't require auth)"""
    try:
        return get_current_user_from_session(request, db)
    finally:
        db.close()


async def require_auth(request: Request, db: Session = next(get_db())) -> User:
    """Dependency that requires authentication"""
    try:
        user = get_current_user_from_session(request, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        return user
    finally:
        db.close()
