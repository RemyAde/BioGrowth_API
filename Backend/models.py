from tortoise import Model, fields
from pydantic import BaseModel
from datetime import datetime, UTC
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    password = fields.CharField(max_length=200, null=False)
    first_name = fields.CharField(max_length=30, null=False)
    last_name = fields.CharField(max_length=30, null=False)
    phone_number = fields.CharField(max_length=20, null=False)
    is_verified = fields.BooleanField(default=False)
    role = fields.CharField(max_length=20, null=False, default="customer")
    join_date = fields.DatetimeField(auto_now_add=True)
    address_id = fields.ForeignKeyField("models.Address", related_name="user")



class Address(Model):
    id = fields.IntField(pk=True, index=True)
    street_address = fields.CharField(max_length=200, null=True)
    city = fields.CharField(max_length=20, null=True)
    state = fields.CharField(max_length=20, null=True)
    country = fields.CharField(max_length=20, null=True)


class Product(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=100, null=False, index=True)
    summary = fields.CharField(max_length=150, null=True)
    description = fields.CharField(max_length=500, null=True)
    key_features = fields.CharField(max_length=400, null = True)
    benefits = fields.CharField(max_length=250, null=True)
    usage = fields.CharField(max_length=250, null=True)
    review = fields.CharField(max_length=400)
    rating = fields.IntField()
    product_image = fields.CharField(max_length=200, null=False, default="productDefault.jpg")
    plan = fields.ForeignKeyField("models.Plan", related_name="products")
    owner = fields.ForeignKeyField("models.User", related_name="products")


class Plan(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=20, null=False, index=True)
    monthly_price = fields.DecimalField(max_digits=12, decimal_places=2)
    annual_price = fields.DecimalField(max_digits=12, decimal_places=2)


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", "role"))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password", "is_verfified", "role", "join_date"))

address_pydantic = pydantic_model_creator(Address, name="Address")
address_pydanticIn = pydantic_model_creator(Address, name="AddressIn", exclude_readonly=True)

product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)

plan_pydantic = pydantic_model_creator(Plan, name="Plan")
plan_pydanticIn = pydantic_model_creator(Plan, name="PlanIn", exclude="owner")
