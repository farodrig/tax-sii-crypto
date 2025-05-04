from rich import print

from models.usd_to_clp_rates import USDToCLPRates


async def load_rates(rates: list[USDToCLPRates]) -> None:
    rate_dates = set([r.date for r in rates])
    existing_rates = await USDToCLPRates.filter(date__in=rate_dates)
    existing_rates_dict = {r.date: r for r in existing_rates}

    to_create_rates = [r for r in rates if r.date not in existing_rates_dict.keys()]
    if to_create_rates:
        print(f"Loading {len(to_create_rates)} new rates into the database")
        await USDToCLPRates.bulk_create(to_create_rates, batch_size=500)

    to_update_rates = []
    for r in rates:
        if r.date not in existing_rates_dict.keys():
            continue
        existing_rate = existing_rates_dict[r.date]
        r.pk = existing_rate.pk
        to_update_rates.append(r)

    if to_update_rates:
        print(f"Updating {len(to_update_rates)} rates into the database")
        await USDToCLPRates.bulk_update(
            to_update_rates,
            fields=["date", "value"],
            batch_size=500,
        )
