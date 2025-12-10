import duckdb
import pandas as pd

from src.models import ValidateResponse
from src.services.db_service import DbService
from src.services.google_sheets_service import GoogleSheetsService

conn = duckdb.connect(database=':memory:')


class ValidationService(object):

    def __init__(self) -> None:
        self.google_sheets_service: GoogleSheetsService = GoogleSheetsService()
        self.db_service: DbService = DbService()

    async def validate_async(self, event_type: str, url: str) -> ValidateResponse:

        rules = await self.db_service.get_validation_rules(event_type=event_type)

        all_tables = [table_name for tables in rules.values() for table_name in tables]

        db_tables = {}
        for table in all_tables:

            data = await self.db_service.get_all(table)
            db_tables[table] = data

        sheets_data = await self.google_sheets_service.fetch_sheet_data(url=url)

        self.insert_to_duckdb(sheets_data, db_tables)

        results = []

        for rule in rules.keys():

            invalid_rows = conn.execute(rule.query).fetchdf()

            if invalid_rows.empty:
                continue

            results.append(rule.error_message)

        return ValidateResponse(status="invalid", errors=results) \
            if len(results) > 0 else ValidateResponse(
            status="valid", errors=[])

    async def fetch_db_data(self, tables: list[str]) -> pd.DataFrame:
        ...

    def insert_to_duckdb(self, sheet_tabs: dict[str, pd.DataFrame], db_tables: dict[str, pd.DataFrame]) -> None:

        for tab_name, df in sheet_tabs.items():

            conn.execute(f"CREATE TABLE IF NOT EXISTS {tab_name} AS SELECT * FROM df")
            conn.register(tab_name, df)

        for table_name, df in db_tables.items():

            conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
            conn.register(table_name, df)
