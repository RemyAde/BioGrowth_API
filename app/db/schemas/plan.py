from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.plan import Plan

plan_pydantic = pydantic_model_creator(Plan, name="Plan")
plan_pydanticIn = pydantic_model_creator(Plan, name="PlanIn", exclude_readonly=True)
