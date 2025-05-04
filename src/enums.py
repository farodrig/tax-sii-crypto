from enum import StrEnum, auto


class Currency(StrEnum):
    USDC = auto()
    USDT = auto()
    BTC = auto()
    CLP = auto()


class Market(StrEnum):
    BTC_USDC = auto()
    BTC_CLP = auto()
    USDC_CLP = auto()


class OperationType(StrEnum):
    BUY = auto()
    SELL = auto()
    TRANSFER = auto()
    DEPOSIT = auto()
    WITHDRAW = auto()


class TransactionType(StrEnum):
    BUY = auto()
    SELL = auto()
    TRANSFER = auto()
    DEPOSIT = auto()
    WITHDRAW = auto()
    BUY_FEE = auto()
    SELL_FEE = auto()
    TRANSFER_FEE = auto()
