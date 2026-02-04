import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class GoogleSheetsService(object):

    __slots__ = (
        "creds",
        "gc",
    )

    def __init__(self):
        self.creds = Credentials.from_service_account_info(
            {

            }, scopes=SCOPES)
        self.gc = gspread.authorize(self.creds)

    async def fetch_sheet_data(self, url: str) -> dict[str, pd.DataFrame]:

        # spreadsheet_id = url.split("/d/")[1].split("/")[0]

        sh = self.gc.open_by_url(url)

        dfs = {}
        for ws in sh.worksheets():
            if ws.isSheetHidden:
                continue
            values = ws.get_all_values()
            if not values:
                dfs[ws.title] = pd.DataFrame()
                continue
            header, rows = values[0], values[1:]
            dfs[ws.title] = pd.DataFrame(rows, columns=header)
            # add id column if not exists
            if "id" not in dfs[ws.title].columns:
                dfs[ws.title].insert(0, "Id", range(1, len(dfs[ws.title]) + 1))
        return dfs
