import pandas as pd

from src.models import Rule


class DbService(object):


    async def get_validation_rules(self, event_type: str) -> dict[Rule, list[str]]:
        ...

    async def get_all_tables_names(self) -> list[str]:
        ...

    async def get_all(self, table_name: str) -> pd.DataFrame:
        ...