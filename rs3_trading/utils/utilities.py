import duckdb
import pandas as pd
import requests

from rs3_trading.database.ge_tick_database import create_price_table, create_volume_table, insert_into_price_table, insert_into_volume_table


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
    con = duckdb.connect('GE_Tick_Data')
    create_price_table(con)
    create_volume_table(con)
    con.close()


def most_recent_database_update_time() -> int:
    con = duckdb.connect('GE_Tick_Data')
    most_recent_time = con.execute('select max(time) as time from rs3_price_data').df().time[0].timestamp()
    con.close()
    return int(most_recent_time)


def update_database(url_price: str, url_volume: str):
    print("Updating database...")
    con = duckdb.connect('GE_Tick_Data')
    most_recent_time = most_recent_database_update_time()

    price_data = data_retrieval(url_price)
    unix_time_price = pop_unix_time_from_dict(price_data)

    if unix_time_price > most_recent_time:
        ge_tick_dataframe_price = transform_to_dataframe(price_data, unix_time_price, 'price')
        insert_into_price_table(con, ge_tick_dataframe_price)
    else:
        print('There is currently no updated data')

    volume_data = data_retrieval(url_volume)
    unix_time_volume = pop_unix_time_from_dict(volume_data)

    if unix_time_volume > most_recent_time:
        ge_tick_dataframe_volume = transform_to_dataframe(volume_data, unix_time_volume, 'volume')
        insert_into_volume_table(con, ge_tick_dataframe_volume)
    else:
        print('There is currently no updated data')

    con.close()
