from core.config import settings

DATABASE_URL = settings.DATABASE_URL


TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "app.db.models.user",
                "app.db.models.address",
                "app.db.models.plan",
                "app.db.models.product",
                "app.db.models.cart"
            ],
            "default_connection": "default"
        },
    },
}