from fastapi import Depends, HTTPException
from db.models.cart import Cart


async def check_cart_validity(cart_id, user):
    cart_items = await Cart.filter(owner = user)
    if cart_items:
        cart_ids = [cart.id for cart in cart_items]
        if cart_id in cart_ids:
            cart_obj = await Cart.get_or_none(id = cart_id)
            return {
                "status":"ok",
                "data":cart_obj
            }
        return {
            "status": "error",
            "error": "cart item not found"
        }
    return {
        "status": "error",
        "error": "You haven't added an item to your cart"
    }