import csv
from datetime import date
from pathlib import Path

from rich.progress import track


def extract_usd_to_clp_rates(file_path: Path, year: int) -> list[tuple[date, float]]:
    """
    Extracts USD to CLP conversion rates from a CSV file.

    Args:
        file_path (Path): The path to the CSV file.

    Returns:
        list[dict[date, float]]: A list of dictionaries containing the date and conversion rate.
    """
    rates = []
    with open(file_path, newline="") as csvfile:
        rows_length = len(csvfile.readlines()) - 1
        csvfile.seek(0)
        reader = csv.reader(csvfile, delimiter=";")
        next(reader, None)
        for row in track(reader, description="Processing rates", total=rows_length):
            if row[0] == "Promedio":
                continue
            day = int(row[0])
            for month in range(1, 13):
                if not row[month]:
                    continue
                rate = float(row[month].replace(".", "").replace(",", "."))
                rates.append((date(year, month, day), rate))
    return rates
