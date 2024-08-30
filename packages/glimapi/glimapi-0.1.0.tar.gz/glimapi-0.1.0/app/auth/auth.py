from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthMiddleware:
    def __init__(self, settings):
        self.settings = settings
        self.bearer = HTTPBearer()

    async def __call__(self, request: Request, call_next):
        if request.url.path not in ["/login", "/signup"]:
            credentials: HTTPAuthorizationCredentials = await self.bearer(request)
            if credentials:
                try:
                    payload = jwt.decode(
                        credentials.credentials,
                        self.settings.auth["secret_key"],
                        algorithms=[self.settings.auth["algorithm"]]
                    )
                except JWTError:
                    raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        response = await call_next(request)
        return response

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=settings.auth["access_token_expire_minutes"])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth["secret_key"], algorithm=settings.auth["algorithm"])
    return encoded_jwt
