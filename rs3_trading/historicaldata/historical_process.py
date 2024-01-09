import asyncio
import json
import logging
import urllib
from collections import deque
from time import sleep
from typing import Any, Coroutine, Iterable

import pandas as pd
import requests

from rs3_trading.database.dbcm import DuckDBCM
from rs3_trading.historicaldata.historical_utils import extract_item_name_from_table, historical_data_transformation
from rs3_trading.historicaldata.request_errors import check_request_status, NotFoundError, RequestTimeoutError, TooManyRequestsError
from rs3_trading.utils.utilities import create_database_tables, insert_into_table, join_with_commas

LOG_FILE = 'historicaldata_log.log'

API_URL = 'https://api.weirdgloop.org/exchange/history/rs/last90d?name='


query_string = 'select item_name from rs3_price_data'
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

item_names: deque = extract_item_name_from_table(query_string, 'GE_Tick_Data.db')
create_database_tables()


async def task_query_rs_api_for_item(item_name: str) -> pd.DataFrame:
    """"Define a task."""
    encoded_item_name = urllib.parse.quote(item_name)
    url = f'{API_URL}{encoded_item_name}'
    response = requests.get(url)
    check_request_status(response)

    try:
        if len(response.content) == 0:
            return pd.DataFrame()

        historical_data_json = response.json()

    except json.JSONDecodeError as e:
        logging.error(f'JSONDecodeError: {str(e)}')

    historical_data_df = historical_data_transformation(historical_data_json, item_name)
    return historical_data_df


def batch_tasks(tasks: Iterable[Coroutine[Any, Any, Any]], batch_size: int):
    """Take an iterable and return an iterable that consumes a batch of size n."""
    length = len(tasks)
    for index in range(0, length, batch_size):
        yield tasks[index:min(index + batch_size, length)]


async def main(database_name: str, batch_size: int) -> None:

    task_set = list(map(task_query_rs_api_for_item, item_names))
    count = 0
    for batch in batch_tasks(task_set, batch_size):
        try:
            results: pd.DataFrame = pd.concat(await asyncio.gather(*batch))

        except TooManyRequestsError as e:
            logging.error(f'TooManyRequestsError: {str(e)}')
            print('TooManyRequestsError: Waiting for 1400 seconds before retrying.')
            sleep(1400)
        except NotFoundError as e:
            logging.error(f'NotFoundError: {str(e)}')
        except RequestTimeoutError as e:
            logging.error(f'RequestTimeoutError: {str(e)}')

        for _ in range(batch_size):
            item_names.popleft()

        with DuckDBCM(database_name) as con:
            columns = list(results.columns)
            columns_str = join_with_commas(columns)
            insert_into_table(con, 'rs3_historical_data', columns_str, results)

        count += batch_size
        print(f'Processed {count} requests.')
        sleep(20)
