from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from dotenv import dotenv_values

app = FastAPI()

config_credentials = dotenv_values(".env")

@app.get("/")
def index():
    return {"message":"hello world"}


register_tortoise(
    app=app,
    db_url=config_credentials["DATABASE_URL"],
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)