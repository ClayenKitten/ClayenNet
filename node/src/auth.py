from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import Configuration

security = HTTPBearer()

def verify_token(
    authorization: HTTPAuthorizationCredentials = Depends(security),
    config: Configuration = Depends()
) -> None:
    if not authorization.credentials.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid authorization header")
    token = authorization.credentials.split(" ", 1)[1]
    if token != config.api_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
