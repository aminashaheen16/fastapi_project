from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from services.jwt_service import verify_token

scheme = HTTPBearer()

async def get_current_user(credentials = Depends(scheme)) -> str:
    """Verify JWT token"""
    token = credentials.credentials
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id
