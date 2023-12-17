import pandas as pd
from duckdb import DuckDBPyConnection


def create_price_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_price_data(time datetime, item varchar, item_name varchar, price long, primary key(item, time))')


def create_volume_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_volume_data(time datetime, item varchar, item_name varchar, volume long, primary key(item, time))')


def insert_into_table(con: DuckDBPyConnection, table_name: str, column_names: list, dataframe: pd.DataFrame):
    con.execute("""insert into {table_name}({column_names})
            select
                time,
                item,
                item_name,
                price
            from {dataframe}""")
