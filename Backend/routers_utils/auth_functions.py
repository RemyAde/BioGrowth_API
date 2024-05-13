from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
from models import User
from dotenv import dotenv_values

config_credentials = dotenv_values(".env")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hashed_password(password):
    return pwd_context.hash(password)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config_credentials["secret_key"], algorithms=config_credentials["algorithm"])
        user = await User.get(id = payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user