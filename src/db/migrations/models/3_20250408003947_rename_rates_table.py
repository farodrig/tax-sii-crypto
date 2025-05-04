from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usdtoclprates" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL UNIQUE,
    "value" DOUBLE PRECISION NOT NULL
);
        DROP TABLE IF EXISTS "usdtoclpconversion";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "usdtoclprates";"""
