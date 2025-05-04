from collections import defaultdict
from typing import TypeVar

from tortoise.exceptions import ObjectDoesNotExistError

from models.usd_to_clp_rates import USDToCLPRates

T = TypeVar("T")


def group_by(item_list: list[T], key=lambda x: x) -> dict[T, list[T]]:
    d = defaultdict(list)
    for item in item_list:
        d[key(item)].append(item)
    return d.items()


async def usd_to_clp(value: float, date: str) -> float:
    rate = await USDToCLPRates.filter(date__lte=date).order_by("-date").first()
    if not rate:
        raise ObjectDoesNotExistError(USDToCLPRates, "date", date)
    return value * rate.value
