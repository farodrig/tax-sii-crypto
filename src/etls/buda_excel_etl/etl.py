from pathlib import Path

from rich import print

from etls.buda_excel_etl.loader import load_data
from etls.buda_excel_etl.transformer import rows_to_models
from parsers.excel import get_rows


async def main(file_path: Path) -> None:
    """
    Main function to read an Excel file and print its content.

    Args:
        file_path (Path): The path to the Excel file.
    """
    print(f"Loading data from {file_path}")
    rows = get_rows(file_path)

    print("Creating models from rows")
    [operations, transactions] = rows_to_models(rows)

    print("Loading data into the database")
    await load_data(operations, transactions)
