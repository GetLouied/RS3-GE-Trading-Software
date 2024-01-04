import pandas as pd
from duckdb import DuckDBPyConnection


def create_price_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_price_data(datetime_utc datetime, item varchar, item_name varchar, price long, primary key(item, datetime_utc))')


def create_volume_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_volume_data(datetime_utc datetime, item varchar, item_name varchar, volume long, primary key(item, datetime_utc))')


def create_historical_data_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_historical_data(id int, datetime_utc datetime, price long, volume long)')


def create_id_item_name_table(con: DuckDBPyConnection):
    con.execute('create table if not exists rs3_ids_and_item_names(id int, item_name varchar)')


def insert_into_table(con: DuckDBPyConnection, table_name: str, column_names: str, _: pd.DataFrame):
    con.execute(f"""insert into {table_name}({column_names})
            select
                {column_names}
            from _""")
