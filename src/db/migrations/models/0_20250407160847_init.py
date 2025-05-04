from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "operation" (
    "id" UUID NOT NULL PRIMARY KEY,
    "executed_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "market" VARCHAR(100),
    "market_value" DOUBLE PRECISION,
    "operation_type" VARCHAR(100) NOT NULL
);
COMMENT ON COLUMN "operation"."market" IS 'Market where the operation was executed';
COMMENT ON COLUMN "operation"."market_value" IS 'Market value at the moment of the operation';
COMMENT ON COLUMN "operation"."operation_type" IS 'Type of operation performed';
CREATE TABLE IF NOT EXISTS "transaction" (
    "id" UUID NOT NULL PRIMARY KEY,
    "executed_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "balance" DOUBLE PRECISION NOT NULL,
    "currency" VARCHAR(10) NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,
    "transaction_type" VARCHAR(100) NOT NULL,
    "operation_id" UUID NOT NULL REFERENCES "operation" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "transaction"."balance" IS 'Balance at the end of the transaction';
COMMENT ON COLUMN "transaction"."currency" IS 'Currency of the transaction';
COMMENT ON COLUMN "transaction"."amount" IS 'Amount of the transaction';
COMMENT ON COLUMN "transaction"."transaction_type" IS 'Type of operation performed';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
