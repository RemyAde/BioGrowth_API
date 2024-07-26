from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.cart import Cart


cart_pydantic = pydantic_model_creator(Cart, name="Cart")
cart_pydanticIn = pydantic_model_creator(Cart, name="CartIn", exclude_readonly=True, exclude=("quantity",))