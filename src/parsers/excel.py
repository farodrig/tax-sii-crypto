from pathlib import Path
from typing import Any

import pyexcel


def get_rows(file_path: Path) -> list[dict[str, Any]]:
    """
    Reads an Excel file and returns its content as a list of dictionaries.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        list: A list of dictionaries representing the rows in the Excel file.
    """
    records = pyexcel.get_records(file_name=str(file_path))
    pyexcel.free_resources()
    return records
