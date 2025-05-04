# Tax SII Crypto

A Python-based tool for processing cryptocurrency transactions, generating buy/sell reports, and managing USD to CLP exchange rates. This project uses Tortoise ORM for database management and supports ETL processes for loading and transforming data from Excel and CSV files.
For now, this is especifically created for chilean SII calculation and Buda.com

<a href="https://ko-fi.com/farodrig" target="_blank">
  <img src="https://github.com/user-attachments/assets/c9ac045b-faea-4fac-ac6a-3820fa07b473" alt="Alt Text" height="50">
</a>


## Features

- **ETL Pipelines**:
  - Load cryptocurrency transactions from Excel files (Buda format).
  - Load USD to CLP exchange rates from CSV files (SII format).
  - Transform and store data in a database.

- **Reports**:
  - Generate buy/sell reports for cryptocurrency transactions (For Buda SII excel calculations).
  - Export reports to Excel files.

- **Database Management**:
  - Uses Tortoise ORM for database operations.
  - Supports PostgreSQL and SQLite.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/tax-sii-crypto.git
   cd tax-sii-crypto
   ```

2. Install dependencies:
    ```bash
    pip install poetry
    poetry install
    ```

3. Set up the environment variables:
    - Copy .env.example to .env and update the DB_URL with your database connection string.

4. Run database migrations:
    ```bash
    poetry run aerich upgrade
    ```

## Usage
You can run `poetry run python src/main.py --help` to get the list of available commands.

### Load Cryptocurrency Transactions
Load transactions from an Excel file:
```bash
poetry run python src/main.py load-buda-transactions <path_to_excel_file>
```

### Load USD to CLP Exchange Rates
Load exchange rates for a specific year:
```bash
poetry run python src/main.py load-sii-usd-to-clp-rates <path_to_csv_file> <year>
```

Load all preloaded exchange rates:
```bash
poetry run python src/main.py load-all-sii-usd-to-clp-rates
```

### Generate Buy/Sell Report
Generate a report and optionally load exchange rates:
```bash
poetry run python src/main.py generate-buy-sells-report --load-rates --filename <output_filename>
```

## Development
### Run Tests
Run the test suite with coverage:
```bash
poetry run pytest --cov=src
```

### Linting
Use Ruff to check issues codebase:
```bash
poetry run ruff check
```

### Formatting
Use Ruff to format the codebase:
```bash
poetry run ruff format
```

## Important
This code is not production ready. Be careful using it, the results could be wrong.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Felipe Rodríguez
