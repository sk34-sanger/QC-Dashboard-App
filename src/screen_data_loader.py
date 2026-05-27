"""Load screen datasets from PostgreSQL tables."""

from __future__ import annotations

import pandas as pd

from db import get_db_schema, read_table
from screen_tables import SCREEN_DATASET_TABLES


def load_screen_dataframes(schema: str | None = None) -> dict[str, pd.DataFrame]:
    """Return all DataFrames needed by the screen page."""
    active_schema = schema or get_db_schema()
    return {
        key: read_table(table_name=table_name, schema=active_schema)
        for key, table_name in SCREEN_DATASET_TABLES.items()
    }
