from uuid import uuid4  # noqa: N999

from tortoise.fields import CharEnumField, DatetimeField, FloatField, ForeignKeyRelation, UUIDField
from tortoise.models import Model

from enums import Currency, TransactionType
from errors import CurrencyError
from utils import usd_to_clp


class Transaction(Model):
    id = UUIDField(default=uuid4, primary_key=True)
    operation = ForeignKeyRelation("models.Operation", related_name="transactions")
    executed_at = DatetimeField(auto_now_add=True)
    balance = FloatField(
        description="Balance at the end of the transaction",
    )
    currency = CharEnumField(
        enum_type=Currency,
        description="Currency of the transaction",
        max_length=10,
    )
    amount = FloatField(
        description="Amount of the transaction",
    )
    transaction_type = CharEnumField(
        enum_type=TransactionType,
        description="Type of operation performed",
        max_length=100,
    )


async def get_amount_in_clp(transaction: Transaction) -> float:
    """
    Calculate the equivalent amount in CLP for a given transaction.

    Args:
        transaction (Transaction): The transaction to convert.

    Returns:
        float: The equivalent amount in CLP.
    """
    if transaction.currency == Currency.CLP:
        return transaction.amount
    elif transaction.currency == Currency.USDT:
        return await usd_to_clp(transaction.amount, transaction.executed_at)
    elif transaction.currency == Currency.USDC:
        return await usd_to_clp(transaction.amount, transaction.executed_at)
    else:
        raise CurrencyError(transaction.currency)
