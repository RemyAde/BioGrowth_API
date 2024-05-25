from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.product import Product
from pydantic import BaseModel


product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True, exclude=("product_image","rating"))