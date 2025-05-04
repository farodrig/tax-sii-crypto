from models.usd_to_clp_rates import USDToCLPRates


def get_db_rates(rates: list[tuple[str, float]]) -> list[USDToCLPRates]:
    return [
        USDToCLPRates(
            date=rate[0],
            value=rate[1],
        )
        for rate in rates
    ]
