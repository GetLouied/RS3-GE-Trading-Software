import duckdb
import pandas as pd
import requests

url = "https://runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"


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


con = duckdb.connect('GETest')


def create_ge_tick_table(con):
    con.execute('create table if not exists ge_tick_data(time datetime, item varchar, item_name varchar, price long)')


def insert_into_tick_table(con, ge):
    con.execute("""insert into ge_tick_data(time, item, item_name, price)
            select
                time,
                item,
                item_name,
                price
            from ge""")


# Create a util folder for the above functions
# Create a main.py that calls these functions in the right order and include fast api in your main function
