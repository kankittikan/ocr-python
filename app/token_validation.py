import os
import jwt
from fastapi import HTTPException, Request

SECRET_KEY = os.getenv('SECRET')

def verify_access_token(request):
    token = request.headers.get("access_token")
    if not token:
        raise HTTPException(status_code=400, detail="Required access token")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")