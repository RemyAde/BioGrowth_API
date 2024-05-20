from tortoise.contrib.pydantic import pydantic_model_creator
from models.address import Address


address_pydantic = pydantic_model_creator(Address, name="Address")
address_pydanticIn = pydantic_model_creator(Address, name="AddressIn", exclude_readonly=True)