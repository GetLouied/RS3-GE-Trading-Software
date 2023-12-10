import pandas as pd
import requests


def data_retrieval(url: str) -> dict:
    r = requests.get(url)
    data = r.json()
    return data


def time_retrieval(data: dict) -> int:
    unix_time = data.pop('%LAST_UPDATE%')
    data.pop('%LAST_UPDATE_F%')
    return unix_time


def transform_to_dataframe(data: dict, unix_time: int) -> pd.DataFrame:
    column_names = ['item_name', 'price']
    ge = pd.DataFrame.from_dict(data, orient='index').reset_index()
    ge.columns = column_names
    ge['time'] = pd.to_datetime(unix_time, unit='s')
    ge['item'] = ge['item_name'].str.lower().replace('[^A-Za-z0-9+()]+', '', regex=True)
    return ge
