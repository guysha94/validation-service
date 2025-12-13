import pandas as pd
from sqlalchemy import inspect

from ..db import engine
from ..rules.models import Rule


class DbService(object):


    async def get_validation_rules(self, event_type: str) -> dict[Rule, list[str]]:
        ...

    @classmethod
    async def get_table_names(cls, schema: str = "backend") -> list[str]:
        async with engine.connect() as conn:
            return await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names(schema=schema)
            )

    async def get_all(self, table_name: str) -> pd.DataFrame:
        ...
