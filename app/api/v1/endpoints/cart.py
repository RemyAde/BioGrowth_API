from fastapi import APIRouter, HTTPException, Depends, status
from db.models.cart import Cart
from db.models.product import Product
from db.schemas.cart import cart_pydantic, cart_pydanticIn
from db.schemas.user import user_pydantic

from api.v1.dependencies.auth import get_current_user
from api.v1.dependencies.cart import check_cart_validity


router = APIRouter(
    prefix="/cart",
    tags=["/cart"]
)


@router.get("/")
async def list_cart(user: user_pydantic = Depends(get_current_user)): # type: ignore
    cart_items = await Cart.filter(owner=user)
    return {
        "status": "ok",
        "data": cart_items
    }

@router.post("/add")
async def create_cart(product_id: int, cart_request: cart_pydanticIn, user: user_pydantic = Depends(get_current_user)): # type: ignore
    cart_request = cart_request.dict(exclude_unset = True)

    product_obj = await Product.get_or_none(id = product_id)
    cart_obj = await Cart.create(**cart_request, product=product_obj, owner=user)
    response = await cart_pydantic.from_tortoise_orm(cart_obj)

    return {
        "status":"ok",
        "data": response
    }


@router.get("/{cart_id}")
async def retreive_cart(cart_id: int, user: user_pydantic = Depends(get_current_user)): # type: ignore
    result = await check_cart_validity(cart_id, user)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@router.put("/increase/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def increase_cart(cart_id: int, user: user_pydantic = Depends(get_current_user)): # type: ignore
    result = await check_cart_validity(cart_id, user)
    if result["status"] == "ok":
        cart_obj = result["data"]
        cart_obj.quantity = cart_obj.quantity + 1
        await cart_obj.save()
        return 
    
    elif result["status"] == "error":
        raise HTTPException (
            status_code=404, 
            detail=result["error"]
        )
 

@router.put("/decrease/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def decrease_cart(cart_id: int, user: user_pydantic = Depends(get_current_user)): # type: ignore
    result = await check_cart_validity(cart_id, user)
    if result["status"] == "ok":
        cart_obj = result["data"]
        if cart_obj.quantity == 1:
            await cart_obj.delete()
        elif cart_obj.quantity > 1:
            cart_obj.quantity = cart_obj.quantity - 1
            await cart_obj.save()
    
    elif result["status"] == "error":
        raise HTTPException (
            status_code=404, 
            detail=result["error"]
        )
    

@router.delete("/delete/{cart_id}", status_code=204)
async def delete_cart_item(cart_id: int, user: user_pydantic = Depends(get_current_user)): # type: ignore
    result = await check_cart_validity(cart_id, user)
    if result["status"] == "ok":
        cart_obj = result["data"]
        await cart_obj.delete()
    
    elif result["status"] == "error":
        raise HTTPException (
            status_code=404, 
            detail=result["error"]
        )
    