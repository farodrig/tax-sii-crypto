import os

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DB_URL", "sqlite://db.sqlite3")},
    "apps": {
        "models": {
            "models": [
                "models.operation",
                "models.transaction",
                "models.usd_to_clp_rates",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
