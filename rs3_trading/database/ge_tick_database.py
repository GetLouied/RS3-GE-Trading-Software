import pandas as pd
from duckdb import DuckDBPyConnection


def create_price_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_price_data(datetime_utc datetime, item varchar, item_name varchar, price long, primary key(item, datetime_utc))')


def create_volume_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_volume_data(datetime_utc datetime, item varchar, item_name varchar, volume long, primary key(item, datetime_utc))')


def insert_into_table(con: DuckDBPyConnection, table_name: str, column_names: list, dataframe: pd.DataFrame):
    columns_str = ", ".join(column_names)
    con.execute(f"""insert into {table_name}({columns_str})
            select
                {columns_str}
            from dataframe""")
