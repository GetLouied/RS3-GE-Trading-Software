from collections import deque

import pandas as pd

from rs3_trading.database.dbcm import DuckDBCM


def extract_item_name_from_table(query_string: str, file_name: str) -> pd.Series:
    with DuckDBCM(file_name) as con:
        df = con.execute(query_string).df()
        item_names = df['item_name']
        return deque(item_names.values)
