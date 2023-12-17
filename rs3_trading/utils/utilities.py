import pandas as pd
import requests
from duckdb import DuckDBPyConnection

from rs3_trading.contextmanager.contextmanager import DuckDBCM
from rs3_trading.database.ge_tick_database import create_price_table, create_volume_table, insert_into_table
from rs3_trading.utils.database_util import RS3TableBuilder
from rs3_trading.utils.url_utils import RSDataType

DATABASE_NAME = 'GE_Tick_Data.db'


def data_retrieval(url: str) -> dict:
    r = requests.get(url)
    data = r.json()
    return data


def pop_unix_time_from_dict(data: dict) -> int:
    unix_time = data.pop('%LAST_UPDATE%', None)
    data.pop('%LAST_UPDATE_F%', None)
    return unix_time


def transform_to_dataframe(data: dict, unix_time: int, column_name: str) -> pd.DataFrame:
    column_names = ['item_name', column_name]
    ge_tick_dataframe = pd.DataFrame.from_dict(data, orient='index').reset_index()
    ge_tick_dataframe.columns = column_names
    ge_tick_dataframe['time'] = pd.to_datetime(unix_time, unit='s')
    ge_tick_dataframe['item'] = ge_tick_dataframe['item_name'].str.lower().replace('[^A-Za-z0-9+()]+', '', regex=True)
    return ge_tick_dataframe


def create_database():
    with DuckDBCM(file_name=DATABASE_NAME) as con:
        create_price_table(con)
        create_volume_table(con)


def most_recent_database_update_time() -> int:
    with DuckDBCM(file_name=DATABASE_NAME) as con:
        most_recent_time = con.execute('select max(time) as time from rs3_price_data').df().fillna(pd.to_datetime(0)).time[0].timestamp()

    return int(most_recent_time)


def update_database(url_price: str, url_volume: str):
    print("Updating database...")
    with DuckDBCM(file_name=DATABASE_NAME) as con:

        most_recent_time = most_recent_database_update_time()

        price_data = data_retrieval(url_price)
        unix_time_price = pop_unix_time_from_dict(price_data)

        update_prices(con, most_recent_time, price_data, unix_time_price)

        volume_data = data_retrieval(url_volume)
        unix_time_volume = pop_unix_time_from_dict(volume_data)

        update_volumes(con, most_recent_time, volume_data, unix_time_volume)


def update_volumes(con: DuckDBPyConnection, most_recent_time: int, volume_data: pd.DataFrame, unix_time_volume: int):
    if unix_time_volume <= most_recent_time:
        print('There is currently no updated data')
        return

    ge_tick_dataframe_volume = transform_to_dataframe(volume_data, unix_time_volume, 'volume')
    rs3_volume_table_name = RS3TableBuilder.base_database_name(RSDataType.Volumes)
    rs3_volume_column_names = RS3TableBuilder.base_column_names(RSDataType.Volumes)
    insert_into_table(con, rs3_volume_table_name, rs3_volume_column_names, ge_tick_dataframe_volume)


def update_prices(con: DuckDBPyConnection, most_recent_time: int, price_data: pd.DataFrame, unix_time_price: int):
    if unix_time_price <= most_recent_time:
        print('There is currently no updated data')
        return

    ge_tick_dataframe_price = transform_to_dataframe(price_data, unix_time_price, 'price')
    rs3_price_table_name = RS3TableBuilder.base_database_name(RSDataType.Prices)
    rs3_price_column_names = RS3TableBuilder.base_column_names(RSDataType.Prices)
    insert_into_table(con, rs3_price_table_name, rs3_price_column_names, ge_tick_dataframe_price)
