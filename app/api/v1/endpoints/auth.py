from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, status, Depends, Response
from db.schemas.user import *

# Authentication
from core.security import get_hashed_password, verify_token
from api.v1.dependencies.auth import token_generator, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# response classes
from fastapi.responses import HTMLResponse

from utils.email import *

# templates
from fastapi.templating import Jinja2Templates
# from main import templates

# dependencies
from utils.email import send_verfication_email


router = APIRouter(
    prefix="/auth",
    tags=["/auth"]
)

oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/token")
async def generate_token(response: Response, request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    # return {"access_token": token, "token_type": "bearer"}
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True)


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


@router.post("/registration")
async def user_registration(user: user_pydanticIn, background_tasks: BackgroundTasks): # type: ignore
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    # background_tasks.add_task(send_verfication_email, new_user)
    return{
        "status" : "ok",
        "data" : f"""Hello {new_user.username}, thanks for choosing BioGrowth. Please check your email inbox and click on the link to confirm your registration""" 
    }


# @router.get("/verification", response_class=HTMLResponse)
# async def email_verification(request: Request, token: str):
#     user = await verify_token(token)

#     if user and not user.is_verified:
#         user.is_verified = True
#         await user.save()
#         return templates.TemplateResponse("verification.html", {"request": request, "username": user.username})

#     raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token",
#             headers={"WWW-Authenticate": "Bearer"}
#     )