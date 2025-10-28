from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import jwt
from urllib.parse import urlencode

from database import get_db
from replit_auth import oauth, save_or_update_user, get_current_user, ISSUER_URL, REPL_ID
from models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/login")
async def login(request: Request):
    """Redirect to Replit OAuth login"""
    redirect_uri = request.url_for('auth_callback')
    return await oauth.replit.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    """Handle OAuth callback from Replit"""
    try:
        token = await oauth.replit.authorize_access_token(request)
        
        id_token = token.get('id_token')
        if id_token:
            user_claims = jwt.decode(id_token, options={"verify_signature": False})
            user = save_or_update_user(db, user_claims)
            request.session['user_id'] = user.id
        
        return RedirectResponse(url='/')
    except Exception as e:
        return RedirectResponse(url='/auth/error')


@router.get("/logout")
async def logout(request: Request):
    """Log out the current user"""
    request.session.clear()
    
    end_session_endpoint = f"{ISSUER_URL}/session/end"
    encoded_params = urlencode({
        "client_id": REPL_ID,
        "post_logout_redirect_uri": str(request.base_url),
    })
    logout_url = f"{end_session_endpoint}?{encoded_params}"
    
    return RedirectResponse(url=logout_url)


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    """Get current user information"""
    if not user:
        return {"authenticated": False}
    
    return {
        "authenticated": True,
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_image_url": user.profile_image_url
    }


@router.get("/error")
async def auth_error():
    """Handle authentication errors"""
    return {"error": "Authentication failed"}
