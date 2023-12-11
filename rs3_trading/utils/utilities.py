import pandas as pd
import requests


def data_retrieval(url: str) -> dict:
    r = requests.get(url)
    data = r.json()
    return data


def pop_unix_time_from_dict(data: dict) -> int:
    unix_time = data.pop('%LAST_UPDATE%', None)
    data.pop('%LAST_UPDATE_F%', None)
    return unix_time


def transform_to_tick_dataframe(data: dict, unix_time: int) -> pd.DataFrame:
    column_names = ['item_name', 'price']
    ge_tick_dataframe = pd.DataFrame.from_dict(data, orient='index').reset_index()
    ge_tick_dataframe.columns = column_names
    ge_tick_dataframe['time'] = pd.to_datetime(unix_time, unit='s')
    ge_tick_dataframe['item'] = ge_tick_dataframe['item_name'].str.lower().replace('[^A-Za-z0-9+()]+', '', regex=True)
    return ge_tick_dataframe
