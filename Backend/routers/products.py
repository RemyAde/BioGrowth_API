import sys
sys.path.append("..")


from fastapi import APIRouter, Request, HTTPException, status
from .auth import get_current_user
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

# image upload
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

router = APIRouter(
    prefix="/product",
    tags=["/product"]
)


oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/token")

# static file setup config
router.mount("/static", StaticFiles(directory="../static"), name="static")


@router.post("/upload/product_image/{product_id}")
async def create_upload_file(product_id: int, file: UploadFile = File(...),
                             user: user_pydantic = Depends(get_current_user)): # type: ignore

    FILEPATH = "../static/images/"
    filename = file.filename

    # image.png >> ["image", "png"]
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg", "webp"]:
        return {
            "status": "error", 
            "detail": "File extension not allowed"}
    
    # /static/images/5uc53jj53.jpg
    token_name = secrets.token_hex(10)+"."+extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as img_file:
        img_file.write(file_content)

    # PILLOW - scale
    img = Image.open(generated_name)
    # (200, 200) for profile picture
    img = img.resize(size = (300, 500))

    img_file.close()

    product = await Product.get(id = product_id)
    owner = await product.owner

    if owner == user:
        product.product_image = token_name
        await product.save()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"}
            )
    
    file_url = "localhost:8000" + generated_name[1:]
    return {
        "status": "ok",
        "filename": file_url
    }
