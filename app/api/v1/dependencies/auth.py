from fastapi import HTTPException, status, Depends, Request
from db.models.user import *
from fastapi.security import OAuth2PasswordBearer
import jwt
from core.config import settings
from core.security import verify_password


oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


async def authenticate_user(username, password):
    user = await User.get(username = username)

    if user and await verify_password(password, user.password):
        return user
    return False


async def token_generator(username: str, password: str):
    user = await authenticate_user(username, password)

    if not user:
        raise(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenicate": "Bearer"}
            )
        )
    
    token_data = {
        "id": user.id,
        "username": user.username
    }

    token = jwt.encode(token_data, settings.SECRET_KEY, algorithm = settings.ALGORITM)

    return token


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITM])
        user = User.get(id = payload.get("id"))
    except:
        raise(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenicate": "Bearer"}
            )
        )
    
    return await user


async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    return current_user