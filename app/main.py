from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings

app = FastAPI(title="BioGrowth API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include routers
from api.v1.endpoints import products, plan, auth, cart

app.include_router(products.router)
app.include_router(plan.router)
app.include_router(auth.router)
app.include_router(cart.router)


@app.get("/")
def index():
    return {"message":"hello world"}


register_tortoise(
    app=app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["db.models.user",
                        "db.models.address",
                        "db.models.plan",
                        "db.models.product",
                        "db.models.cart"]},
    generate_schemas=True,
    add_exception_handlers=True
)