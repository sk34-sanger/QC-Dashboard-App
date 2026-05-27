"""PostgreSQL helpers for the QC Dashboard."""

from __future__ import annotations

from functools import lru_cache
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.engine import Engine

load_dotenv()


def _build_connection_url() -> str:
    """Build a SQLAlchemy PostgreSQL URL from environment variables."""
    host = os.getenv("QC_DB_HOST", "127.0.0.1")
    port = os.getenv("QC_DB_PORT", "5432")
    database = os.getenv("QC_DB_NAME", "qc_reports")
    user = os.getenv("QC_DB_USER", "postgres")
    password = os.getenv("QC_DB_PASSWORD", "")

    if password:
        return (
            "postgresql+psycopg2://"
            f"{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{database}"
        )
    return f"postgresql+psycopg2://{quote_plus(user)}@{host}:{port}/{database}"


def get_db_schema() -> str:
    """Get the target schema used for screen tables."""
    return os.getenv("QC_DB_SCHEMA", "public")


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Return a cached SQLAlchemy engine."""
    return create_engine(_build_connection_url(), pool_pre_ping=True)


def read_table(table_name: str, schema: str | None = None) -> pd.DataFrame:
    """Read an entire table into a pandas DataFrame."""
    active_schema = schema or get_db_schema()
    engine = get_engine()
    metadata = MetaData(schema=active_schema)
    table = Table(table_name, metadata, autoload_with=engine)
    df = pd.read_sql(select(table), con=engine)
    if "__row_id" in df.columns:
        return df.drop(columns=["__row_id"])
    return df
