from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.user import User
from pydantic import BaseModel


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", "role"))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True, exclude=("is_verified", "role", "join_date", "profile_image"))
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password", "is_verfified", "role",))