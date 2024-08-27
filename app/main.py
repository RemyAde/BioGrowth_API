from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings

app = FastAPI(title="BioGrowth API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5500","https://biogrowwth.netlify.app/",],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)