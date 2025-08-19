from tortoise import Tortoise
from app.config import settings

async def init_db():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)  # 👈 auto-creates tables if missing

async def close_db():
    await Tortoise.close_connections()
