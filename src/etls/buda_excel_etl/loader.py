from rich import print
from tortoise.transactions import atomic

from models.operation import Operation
from models.transaction import Transaction


async def load_operations(operations: list[Operation]) -> None:
    """
    Load operations into the database.
    """
    operation_ids = [op.id for op in operations]
    existing_operation_ids = set(
        await Operation.filter(id__in=operation_ids).values_list(
            "id",
            flat=True,
        )
    )
    to_create_operations = [op for op in operations if op.id not in existing_operation_ids]
    if to_create_operations:
        print(f"Loading {len(to_create_operations)} new operations into the database")
        await Operation.bulk_create(to_create_operations, batch_size=500)

    to_update_operations = [op for op in operations if op.id in existing_operation_ids]
    if to_update_operations:
        print(f"Updating {len(to_update_operations)} operations into the database")
        await Operation.bulk_update(
            to_update_operations,
            fields=["executed_at", "market", "market_value", "operation_type"],
            batch_size=500,
        )


async def load_transactions(transactions: list[Transaction]) -> None:
    """
    Load transactions into the database.
    """
    transaction_ids = [t.id for t in transactions]
    existing_transaction_ids = set(
        await Transaction.filter(id__in=transaction_ids).values_list(
            "id",
            flat=True,
        )
    )
    to_create_transactions = [t for t in transactions if t.id not in existing_transaction_ids]
    if to_create_transactions:
        print(f"Loading {len(to_create_transactions)} new transactions into the database")
        await Transaction.bulk_create(to_create_transactions, batch_size=500)

    to_update_transactions = [t for t in transactions if t.id in existing_transaction_ids]
    if to_update_transactions:
        print(f"Updating {len(to_update_transactions)} transactions into the database")
        await Transaction.bulk_update(
            to_update_transactions,
            fields=["executed_at", "balance", "currency", "amount", "transaction_type"],
            batch_size=500,
        )


@atomic()
async def load_data(operation: list[Operation], transactions: list[Transaction]) -> None:
    print("Loading operations into the database")
    await load_operations(operation)

    print("Loading transactions into the database")
    await load_transactions(transactions)
