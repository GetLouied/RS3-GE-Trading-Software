from collections import deque

import pandas as pd

from rs3_trading.database.dbcm import DuckDBCM


def extract_item_name_from_table(query_string: str, file_name: str) -> deque:
    with DuckDBCM(file_name) as con:
        df = con.execute(query_string).df()
        item_names = df['item_name']
        return deque(item_names.values)


def historical_data_transformation(historical_data: dict, item_name: str) -> pd.DataFrame:
    historical_data_df = pd.DataFrame.from_dict(historical_data)
    historical_data_transformed = pd.DataFrame(historical_data_df[item_name].values.tolist(), index=historical_data_df.index)
    historical_data_transformed['item_name'] = item_name
    historical_data_transformed.rename(columns={'timestamp': 'datetime_utc'}, inplace=True)
    historical_data_transformed['datetime_utc'] = pd.to_datetime(historical_data_transformed['datetime_utc'], unit='ms', utc=True)
    historical_data_transformed['volume'] = historical_data_transformed['volume'].fillna(0)
    return historical_data_transformed
