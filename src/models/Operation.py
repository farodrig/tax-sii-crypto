from uuid import uuid4  # noqa: N999

from tortoise.fields import CharEnumField, DatetimeField, FloatField, UUIDField
from tortoise.models import Model

from enums import Market, OperationType


class Operation(Model):
    id = UUIDField(default=uuid4, primary_key=True)
    executed_at = DatetimeField(auto_now_add=True)
    market = CharEnumField(
        enum_type=Market,
        description="Market where the operation was executed",
        max_length=100,
        null=True,
    )
    market_value = FloatField(
        description="Market value at the moment of the operation",
        null=True,
    )
    operation_type = CharEnumField(
        enum_type=OperationType,
        description="Type of operation performed",
        max_length=100,
    )
