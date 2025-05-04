from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usdtoclpconversion" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "executed_at" DATE NOT NULL,
    "value" DOUBLE PRECISION NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "usdtoclpconversion";"""
