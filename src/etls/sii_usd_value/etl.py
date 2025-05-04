from pathlib import Path

from rich import print

from etls.sii_usd_value.extractor import extract_usd_to_clp_rates
from etls.sii_usd_value.loader import load_rates as load
from etls.sii_usd_value.transformer import get_db_rates

DIRECTORY = Path(__file__).parent
RATE_FILES_PER_YEAR: dict[int, Path] = {
    2021: DIRECTORY / Path("data/Dolar 2021.csv"),
    2022: DIRECTORY / Path("data/Dolar 2022.csv"),
    2023: DIRECTORY / Path("data/Dolar 2023.csv"),
    2024: DIRECTORY / Path("data/Dolar 2024.csv"),
}


async def load_rates(file_path: Path, year: int) -> None:
    print(f"Loading data from {file_path} for year {year}")
    rows = extract_usd_to_clp_rates(file_path, year)

    print("Creating models from rows")
    rates = get_db_rates(rows)

    print("Loading rates into the database")
    await load(rates)


async def load_all_rates():
    for year, file_path in RATE_FILES_PER_YEAR.items():
        await load_rates(file_path, year)
