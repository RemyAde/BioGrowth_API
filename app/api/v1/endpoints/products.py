from fastapi import APIRouter, Request, HTTPException, status, Depends
from db.models.product import Product
from db.schemas.product import product_pydantic, product_pydanticIn
from db.schemas.user import user_pydantic
from fastapi.responses import JSONResponse
import os

# Authentication
from api.v1.endpoints.auth import get_current_user

# image upload
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

router = APIRouter(
    prefix="/product",
    tags=["/product"]
)

UPLOAD_DIR = "app/static/uploads/products"

@router.post("/upload/product_image/{product_id}")
async def create_upload_file(product_id: int, file: UploadFile = File(...),
                             user: user_pydantic = Depends(get_current_user)): # type: ignore

    filename = file.filename

    # image.png >> ["image", "png"]
    extension = filename.split(".")[1]

    if not file.filename.endswith(("png", "jpg", "jpeg", "webp")):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # /static/images/5uc53jj53.jpg
    token_name = secrets.token_hex(10)+"."+extension
    file_path = os.path.join(UPLOAD_DIR, token_name)
    file_content = await file.read()

    with open(file_path, "wb") as img_file:
        img_file.write(file_content)

    # PILLOW - scale
    img = Image.open(file_path)
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
    
    return JSONResponse(content={"filename": file_path})
    
    # file_url = "localhost:8000" + generated_name
    # return {
    #     "status": "ok",
    #     "filename": file_url
    # }
