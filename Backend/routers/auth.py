import sys
sys.path.append("..")


from fastapi import APIRouter, Request, HTTPException, status
from models import *

# Authentication
from routers_utils.auth_functions import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

# response classes
from fastapi.responses import HTMLResponse

from routers_utils.emails import *

# templates
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["/auth"]
)

oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/token")
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token, config_credentials["secret_key"], algorithms=config_credentials["algorithm"])
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


@router.post("/me")
async def user_login(user: user_pydanticIn = Depends(get_current_user)): # type: ignore
    return {
        "status": "ok",
        "data": {
            "username": user.username,
            "email": user.email,
            "verified": user.is_verified,
            "joined_date": user.join_date.strftime("%b %d %Y")
        }
    }


@post_save(User)
async def send_verfication_email(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
    
    if created:
        await send_email([instance.email], instance)


@router.post("/registration")
async def user_registration(user: user_pydanticIn): # type: ignore
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status" : "ok",
        "data" : f"""Hello {new_user.username}, thanks for choosing BioGrowth. Please check your email inbox and click on the link to confirm your registration""" 
    }


templates = Jinja2Templates(directory="../templates")
@router.get("/verification", response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html", {"request": request, "username": user.username})

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
    )