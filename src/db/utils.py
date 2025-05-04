from tortoise import Tortoise

from db.tortoise_config import TORTOISE_ORM


async def init_db():
    await Tortoise.init(
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    )
    await Tortoise.generate_schemas()


def load_db(func):
    async def wrapper(*args, **kwargs):
        await init_db()
        await func(*args, **kwargs)

    return wrapper
