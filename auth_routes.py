from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
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
        
        user_claims = token.get('userinfo')
        if not user_claims:
            user_claims = await oauth.replit.parse_id_token(request, token)
        
        if user_claims:
            user = save_or_update_user(db, user_claims)
            request.session['user_id'] = user.id
            return RedirectResponse(url='/')
        else:
            print("Error: No user claims found in token")
            return RedirectResponse(url='/auth/error')
        
    except Exception as e:
        error_msg = f"Authentication error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        request.session['auth_error'] = error_msg
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
async def auth_error(request: Request):
    """Handle authentication errors"""
    error_details = request.session.get('auth_error', 'Authentication failed')
    return {"error": error_details}


@router.get("/test")
async def test_oauth():
    """Test OAuth configuration"""
    from replit_auth import REPL_ID, ISSUER_URL
    return {
        "repl_id": REPL_ID[:10] + "..." if REPL_ID else None,
        "issuer_url": ISSUER_URL,
        "oauth_configured": True
    }
