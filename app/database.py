from tortoise import Tortoise

from app.settings.config import Settings

async def init_db():
    await Tortoise.init(config=Settings.TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)  # 👈 auto-creates tables if missing

async def close_db():
    await Tortoise.close_connections()
