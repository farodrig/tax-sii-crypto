from datetime import datetime
from typing import Any

from rich.progress import track

from enums import Currency, Market, OperationType, TransactionType
from models.operation import Operation
from models.transaction import Transaction
from utils import group_by


def get_operation_type_from_transactions(transactions: list[dict[str, Any]]) -> OperationType:
    """
    Get the operation type from a list of transactions.
    """
    transaction_types = {t["detalle"] for t in transactions}
    if "venta" in transaction_types:
        return OperationType.SELL
    elif "compra" in transaction_types:
        return OperationType.BUY
    elif "transferencia" in transaction_types:
        return OperationType.TRANSFER
    elif "retirar" in transaction_types:
        return OperationType.WITHDRAW
    elif "abono" in transaction_types:
        return OperationType.DEPOSIT
    raise ValueError(  # noqa: TRY003
        f"Operation type not found: {transaction_types}"
    )


def get_transaction_type(transaction_type: str) -> TransactionType:  # noqa: PLR0911
    """
    Get the transaction type from a string.
    """
    if "venta" == transaction_type:
        return TransactionType.SELL
    elif "compra" == transaction_type:
        return TransactionType.BUY
    elif "transferencia" == transaction_type:
        return TransactionType.TRANSFER
    elif "retirar" == transaction_type:
        return TransactionType.WITHDRAW
    elif "abono" == transaction_type:
        return TransactionType.DEPOSIT
    elif "comision compra" == transaction_type:
        return TransactionType.BUY_FEE
    elif "comision venta" == transaction_type:
        return TransactionType.SELL_FEE
    raise ValueError(f"Transaction type not found: {transaction_type}")  # noqa: TRY003


def get_operation_from_transactions(transactions: list[dict[str, Any]]) -> Operation:
    """
    Convert a list of transactions to an operation model.
    """
    market_values = [t["precio"] for t in transactions if t["precio"]]
    market_value = max(market_values) if market_values else None
    operation_type = get_operation_type_from_transactions(transactions)
    market_str = transactions[0]["mercado"].replace("-", "_")
    return Operation(
        id=transactions[0]["operacion"],
        executed_at=datetime.strptime(transactions[0]["fecha"], "%Y-%m-%d %H:%M:%S %Z"),
        market=Market[market_str] if market_str else None,
        market_value=market_value,
        operation_type=operation_type,
    )


def row_to_transaction(row: dict[str, Any]) -> Transaction:
    """
    Convert a row from the Excel sheet to a Transaction model.
    """

    return Transaction(
        id=row["id"],
        operation_id=row["operacion"],
        executed_at=datetime.strptime(row["fecha"], "%Y-%m-%d %H:%M:%S %Z"),
        balance=row["balance"],
        currency=Currency[row["moneda"]],
        amount=row["monto"],
        transaction_type=get_transaction_type(row["detalle"]),
    )


def rows_to_models(rows) -> tuple[list[Operation], list[Transaction]]:
    """
    Convert a list of rows from the Excel sheet to a list of dictionary models.
    """
    transactions = [
        row_to_transaction(row) for row in track(rows, description="Processing transactions")
    ]

    operations = [
        get_operation_from_transactions(list(group))
        for _, group in track(
            group_by(rows, lambda x: x["operacion"].strip()),
            description="Processing operations",
        )
    ]
    return [operations, transactions]
