import math
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from rich import print

from enums import Currency, Market, TransactionType
from models.operation import Operation
from models.transaction import Transaction
from utils import usd_to_clp


class TransactionRow(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    year: int
    month: int
    value: float
    transaction: Any


class BuySellRow(BaseModel):
    buy: TransactionRow
    sell: TransactionRow


class Balance(BaseModel):
    transactions_history: list = Field(default_factory=lambda: [])
    clp: float = 0
    btc: float = 0
    usd: float = 0
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

    async def _generate_buy_sell_row(
        self,
        cost_amount: float,
        cost_transaction: Transaction,
        sell_amount: float,
        sell_transaction: Transaction,
    ) -> BuySellRow:
        cost_operation = cost_transaction.operation
        sell_operation = sell_transaction.operation
        cost_value = cost_amount * cost_operation.market_value
        if cost_operation.market == Market.BTC_USDC:
            cost_value = await usd_to_clp(cost_value, cost_operation.executed_at.date())
        sell_value = sell_amount * sell_operation.market_value
        if sell_operation.market == Market.BTC_USDC:
            sell_value = await usd_to_clp(sell_value, sell_operation.executed_at.date())

        return BuySellRow(
            buy=TransactionRow(
                year=cost_operation.executed_at.year,
                month=cost_operation.executed_at.month,
                value=cost_value,
                transaction=cost_transaction,
            ),
            sell=TransactionRow(
                year=sell_operation.executed_at.year,
                month=sell_operation.executed_at.month,
                value=sell_value,
                transaction=sell_transaction,
            ),
        )

    def _add_transaction_to_right_currency(self, transaction: Transaction):
        if transaction.currency == Currency.CLP:
            self.clp += transaction.amount
        elif transaction.currency == Currency.BTC:
            self.btc += transaction.amount
        elif transaction.currency in [Currency.USDC, Currency.USDT]:
            self.usd += transaction.amount

    async def _change_transaction_history_by_selling(
        self, transaction: Transaction
    ) -> list[BuySellRow]:
        should_generate_buy_sell_row = (
            transaction.transaction_type == TransactionType.SELL
            and transaction.currency in [Currency.USDC, Currency.USDT, Currency.BTC]
        )
        to_change_transactions = [
            t for t in self.transactions_history if t.currency == transaction.currency
        ]
        rows = []
        for historic_transaction in to_change_transactions:
            cost_amount = None
            sell_amount = None
            if math.isclose(transaction.amount, 0):
                break

            if historic_transaction.amount > abs(transaction.amount):
                sell_amount = abs(transaction.amount)
                cost_amount = abs(sell_amount)
                historic_transaction.amount += transaction.amount
                transaction.amount = 0
            else:
                sell_amount = abs(historic_transaction.amount)
                cost_amount = abs(sell_amount)
                transaction.amount += historic_transaction.amount
                self.transactions_history.remove(historic_transaction)

            if should_generate_buy_sell_row:
                rows.append(
                    await self._generate_buy_sell_row(
                        cost_amount, historic_transaction, sell_amount, transaction
                    )
                )
        if not math.isclose(transaction.amount, 0):
            print(
                f"Remaining quantity is {transaction.amount}",
                f"for transaction with ID {transaction.id}",
            )

        return rows

    async def add_transaction(self, transaction: Transaction) -> list[BuySellRow]:
        self._add_transaction_to_right_currency(transaction)
        if transaction.amount < 0:
            return await self._change_transaction_history_by_selling(transaction)
        else:
            self.transactions_history = [transaction, *self.transactions_history]

    async def add_operation(self, operation: Operation) -> list[BuySellRow]:
        transactions = (
            await operation.transactions.all().prefetch_related("operation").order_by("-amount")
        )
        rows = []
        for transaction in transactions:
            if new_rows := await self.add_transaction(transaction):
                rows = [*rows, *new_rows]
        return rows
