import asyncio
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

from db.utils import load_db
from etls.buda_excel_etl.etl import main as buda_etl_main
from etls.sii_usd_value.etl import load_all_rates, load_rates
from reports.buy_sells.main import generate_report

load_dotenv()
app = typer.Typer()


@load_db
async def load_data(excel_file_path: Path):
    await buda_etl_main(excel_file_path)


@load_db
async def get_buy_sells_report(filename: str | None, load_rates: bool = False):
    if load_rates:
        await load_all_rates()
    await generate_report(filename)


@app.command()
def load_buda_transactions(excel_file_path: Path):
    asyncio.run(load_data(excel_file_path))


@app.command()
def load_sii_usd_to_clp_rates(excel_file_path: Path, year: str):
    """
    Load the USD to CLP exchange rates from an Excel file for a given year.
    """
    asyncio.run(load_db(load_rates)(excel_file_path, year))


@app.command()
def load_all_sii_usd_to_clp_rates():
    """
    Load all the USD to CLP exchange rates preloaded in the app.
    """
    asyncio.run(load_db(load_all_rates)())


@app.command()
def generate_buy_sells_report(
    load_rates: bool = False,
    filename: Annotated[str | None, typer.Option(help="Filename for the report.")] = None,
):
    """
    Generate the buy/sell report based on the loaded transactions.
    """
    asyncio.run(get_buy_sells_report(filename, load_rates))


if __name__ == "__main__":
    app()
