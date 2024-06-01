from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.product import Product
from pydantic import BaseModel
from decimal import Decimal


product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True, exclude=("product_image","rating"))

class ProductOut(BaseModel):
    id: int
    name: str
    summary: str
    description: str
    key_features: str
    benefits: str
    usage: str
    review: str
    rating: Decimal
    product_image: str
    date_created: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%b %d %Y")
        }