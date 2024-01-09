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
from rs3_trading.utils.utilities import create_database, insert_into_table, join_with_commas

DATABASE_NAME = 'GE_Tick_Data.db'
COLUMN_NAME_ITEM_NAME = 'item_name'
LOG_FILE = 'historicaldata_log.log'

BATCH_SIZE = 5

API_URL = 'https://api.weirdgloop.org/exchange/history/rs/last90d?name='



query_string = f'select {COLUMN_NAME_ITEM_NAME} from rs3_price_data'
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

item_names: deque = extract_item_name_from_table(query_string, DATABASE_NAME)
create_database()


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





async def main():

    task_set = list(map(task_query_rs_api_for_item, item_names))
    count = 0
    for batch in batch_tasks(task_set, BATCH_SIZE):
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

        for _ in range(BATCH_SIZE):
            item_names.popleft()

        with DuckDBCM(DATABASE_NAME) as con:
            columns = list(results.columns)
            columns_str = join_with_commas(columns)
            insert_into_table(con, 'rs3_historical_data', columns_str, results)

        count += BATCH_SIZE
        print(f'Processed {count} requests.')
        sleep(20)



