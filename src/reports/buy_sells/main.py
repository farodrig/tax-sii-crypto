import pyexcel
from rich import print
from rich.progress import track

from models.operation import Operation
from reports.buy_sells.types import Balance, BuySellRow


async def get_current_balance() -> tuple[Balance, list[BuySellRow]]:
    balance = Balance()
    operations = await Operation.all().order_by("executed_at")
    rows = []
    for operation in track(operations, description="Processing operations"):
        if new_rows := await balance.add_operation(operation):
            rows = [*rows, *new_rows]
    return balance, rows


def export_to_excel(rows: list[BuySellRow], filename: str):
    data = [["Año venta", "Mes venta", "Monto venta", "Año compra", "Mes compra", "Monto compra"]]
    for row in rows:
        data.append(
            [
                row.sell.year,
                row.sell.month,
                row.sell.value,
                row.buy.year,
                row.buy.month,
                row.buy.value,
            ]
        )
    pyexcel.save_as(array=data, dest_file_name=filename)


async def generate_report(filename: str | None):
    if filename is None:
        filename = "buy_sells_report.xlsx"

    print("Calculating buy/sell balance")
    [_, rows] = await get_current_balance()

    print(f"Generating report with {len(rows)} rows to {filename}")
    export_to_excel(rows, filename)
