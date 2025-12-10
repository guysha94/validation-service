import pandas as pd


class GoogleSheetsService(object):

    async def fetch_sheet_data(self, url: str) -> dict[str, pd.DataFrame]:
        ...
