import os
from PIL import Image
from fastapi import UploadFile, HTTPException
from db.models.plan import Plan
from db.models.product import Product
from db.schemas.product import product_pydantic, product_pydanticIn


UPLOAD_DIR = "static/uploads/products"


def create_upload_directory():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_file_extension(filename: str):
    extension = filename.split(".")[-1].lower()
    if extension not in ["png", "jpg", "jpeg", "webp"]:
        raise HTTPException(status_code=400, detail="Invalid file format")
    return extension


def save_image(file: UploadFile, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    file_url = "localhost:8000/" + file_path[:]
    with open(file_path, "wb") as img_file:
        img_file.write(file)
    return file_path, file_url


def resize_image(file_path: str):
    img = Image.open(file_path)
    img = img.resize((300, 500))
    img.save(file_path)


async def fetch_product(product_id: int):
    product = await Product.get_or_none(id=product_id)
    return product


async def create_product(product_request, plan_id):
    product_request = product_request.dict(exclude_unset = True)

    plan_obj = await Plan.get(id = plan_id)
    if plan_obj:
        product_obj = await Product.create(**product_request, plan=plan_obj)
        product_obj = await product_pydantic.from_tortoise_orm(product_obj)
        return {
            "status":"ok",
            "data": product_obj
        }
    else:
        return {
            "status": "error",
            "error": "Invalid Plan id"
        }
    

async def retrieve_product_detail(product):
    plan = await product.plan
    response = await product_pydantic.from_tortoise_orm(product)
    return {
        "status":"ok",
        "data":{
            "id": response.id,
            "name":response.name,
            "summary":response.summary,
            "description":response.description,
            "key_features":response.key_features,
            "benefits":response.benefits,
            "usage":response.usage,
            "review":response.review,
            "rating":response.rating,
            "product_image":response.product_image,
            "date_created": response.date_created.strftime("%b %d %Y"),
            "plan":plan.name
        }
    }