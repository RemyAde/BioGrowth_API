import os
from dotenv import load_dotenv

load_dotenv()


class Settings():
    PROJECT_NAME: str = "BioGrowth App"
    PRODUCTION = False
    if PRODUCTION:
        DATABASE_URL: str = os.getenv("PROD_DATABASE_URL")
    else:
        DATABASE_URL: str = os.getenv("DEV_DATABASE_URL")
    SECRET_KEY: str = os.getenv("secret_key")
    ALGORITM: str = os.getenv("algorithm")
    EMAIL: str = os.getenv("email")
    EMAIL_PWD: str = os.getenv("password")

settings = Settings()