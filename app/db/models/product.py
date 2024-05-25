from tortoise import Model, fields
from decimal import Decimal
from pydantic import BaseModel


class Product(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=100, null=False, index=True)
    summary = fields.CharField(max_length=150, null=True)
    description = fields.CharField(max_length=500, null=True)
    key_features = fields.CharField(max_length=400, null = True)
    benefits = fields.CharField(max_length=250, null=True)
    usage = fields.CharField(max_length=250, null=True)
    review = fields.CharField(max_length=400)
    rating = fields.DecimalField(max_digits=1, decimal_places=2, default=Decimal('0.00'))
    product_image = fields.CharField(max_length=200, null=False, default="productDefault.jpg")
    plan = fields.ForeignKeyField("models.Plan", related_name="products")
    date_created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        "product"