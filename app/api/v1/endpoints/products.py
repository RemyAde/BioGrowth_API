from fastapi import APIRouter, Request, HTTPException, status, Depends
from db.models.product import Product
from db.schemas.product import product_pydantic, product_pydanticIn
from db.schemas.user import user_pydantic
from fastapi.responses import JSONResponse

# Authentication
from api.v1.endpoints.auth import get_current_user

# dependencies
from api.v1.dependencies.product import (
    create_product,
    create_upload_directory,
    validate_file_extension,
    save_image,
    resize_image,
    fetch_product_and_plans,
    check_product_plan,
    retrieve_product_detail,
    check_product_owner
)

# image upload
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

router = APIRouter(
    prefix="/product",
    tags=["/product"]
)


@router.get("/")
async def list_products():
    products = await product_pydantic.from_queryset(Product.all())
    return {
        "status":"ok",
        "data":products
    }


@router.post("/create")
async def create_product_endpoint(product_request: product_pydanticIn, plan_id: int, user: user_pydantic = Depends(get_current_user)): # type: ignore
    result = await create_product(product_request, plan_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/upload/product_image/{product_id}")
async def create_upload_file(product_id: int, file: UploadFile = File(...),
                             user: user_pydantic = Depends(get_current_user)): # type: ignore
    filename = file.filename
    validate_file_extension(filename)
    create_upload_directory()
    extension = filename.split(".")[-1]
    token_name = secrets.token_hex(10) + "." + extension
    file_path, file_url = save_image(await file.read(), token_name)
    resize_image(file_path)
    product, plans = await fetch_product_and_plans(product_id, user)
    check_product_plan(product, plans)
    product.product_image = token_name
    await product.save()

    return JSONResponse(content={"filename": file_path, "file_url": file_url})


@router.get("/{product_id}")
async def retreive_product(product_id: int):
    product_obj = await Product.get(id = product_id).prefetch_related("plan")
    if product_obj:
        data = await retrieve_product_detail(product_obj)
        return data
    raise HTTPException(
        status_code=401,
        detail="Product object not found"
    )


@router.put("/{product_id}")
async def edit_product(product_id: int, update_dict: product_pydanticIn, user: user_pydantic = Depends(get_current_user)): # type: ignore
   product, owner = await check_product_owner(product_id, user)
   if product:
        update_dict = update_dict.dict(exclude_unset=True)
        product = await product.update_from_dict(update_dict)
        await product.save()
        data = await retrieve_product_detail(product)
        return data
   else:
        raise HTTPException(
        status_code=404,
        detail="Product not found",
        headers={"WWW-Authenticate": "Bearer"}
        )


@router.delete("/{product_id}")
async def delete_product(product_id: int, user: user_pydantic = Depends(get_current_user)): # type: ignore
    product, owner = await check_product_owner(product_id, user)
    if product and owner==user:
        await product.delete()
        return {"status": "deleted"}
    else:
        return {"error": "Product not found"}