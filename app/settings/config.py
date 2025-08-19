import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_DATABASE = os.getenv("DB_DATABASE", "fastapi_demo")

    TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": DB_HOST,
                    "port": DB_PORT,
                    "user": DB_USER,
                    "password": DB_PASSWORD,
                    "database": DB_DATABASE,
                },
            }
        },
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "default",
            },
        },
        "use_tz": False,
        "timezone": "UTC",
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


settings = Settings()
