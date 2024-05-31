from fastapi import APIRouter, Request, HTTPException, status, Depends
from api.v1.dependencies.auth import get_admin_user
from db.models.plan import Plan
from db.schemas.plan import plan_pydantic, plan_pydanticIn
from db.schemas.user import user_pydantic, user_pydanticIn


router = APIRouter(
    prefix="/plan",
    tags=["/plan"]
)


@router.get("/")
async def list_plans():
    response = await plan_pydantic.from_queryset(Plan.all())
    return {
        "status": "okay",
        "data": response
    }


@router.get("/{plan_id}")
async def get_plan(plan_id: int):
    plan = Plan.get(id = plan_id)
    response = await plan_pydantic.from_queryset_single(plan)

    return {
        "status": "ok",
        "data": response
    }

@router.post("/create")
async def create_plan(plan_request: plan_pydanticIn, user: user_pydantic = Depends(get_admin_user)): # type: ignore
    plan_request = plan_request.dict(exclude_unset = True)

    try:
        # saves object
        plan_obj = await Plan.create(**plan_request, owner=user)
        # return object json
        plan_obj = await plan_pydantic.from_tortoise_orm(plan_obj)

        return {
            "status": "ok",
            "data": plan_obj
        }
    except:
        return {
            "status":"error"
        }
    

@router.delete("/delete/{plan_id}")
async def delete_plan(plan_id: int, user: user_pydantic = Depends(get_admin_user)): # type: ignore
    plan = await Plan.get(id = plan_id)
    if plan:
        await plan.delete()
        return {"status": "deleted"}
    else:
        return {"error": "id matching plan not found"}