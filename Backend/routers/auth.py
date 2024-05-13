import sys
sys.path.append("..")


from fastapi import APIRouter, Request, HTTPException, status
from models import *
from auth_functions import get_hashed_password, verify_token

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

# response classes
from fastapi.responses import HTMLResponse

from emails import *

# templates
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["/auth"]
)

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
        "data" : f"Hello {new_user.username}, thanks for choosing BioGrowth. Please
        check your email inbox and click on the link to confirm your registration" 
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