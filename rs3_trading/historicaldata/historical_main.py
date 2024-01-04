import logging
import urllib
from collections import deque
from time import sleep

import pandas as pd
import requests

from rs3_trading.historicaldata.historical_utils import extract_item_name_from_table
from rs3_trading.historicaldata.request_errors import check_request_status, NotFoundError, RequestTimeoutError, TooManyRequestsError
from rs3_trading.utils.utilities import create_database

DATABASE_NAME = 'GE_Tick_Data.db'
API_URL = 'https://api.weirdgloop.org/exchange/history/rs/last90d?name='
COLUMN_NAME_ITEM_NAME = 'item_name'
LOG_FILE = 'historicaldata_log.log'

query_string = f'select {COLUMN_NAME_ITEM_NAME} from rs3_price_data'
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

create_database()


def query_api_generator(item_names: deque) -> None:
    while item_names:
        item_name = item_names[0]
        encoded_item_name = urllib.parse.quote(item_name)
        url = f'{API_URL}{encoded_item_name}'

        try:
            response = requests.get(url)
            check_request_status(response)
            historical_data = response.json()
            sleep(20)

            historical_data['item_name'] = item_name
            print(historical_data)
            item_name = item_names.popleft()
            yield historical_data

        except TooManyRequestsError as e:
            logging.error(f'TooManyRequestsError: {str(e)}')
            print('TooManyRequestsError: Waiting for 1800 seconds before retrying.')
            sleep(1800)
        except NotFoundError as e:
            logging.error(f'NotFoundError: {str(e)}')
            print(f'NotFoundError for the item_name: {item_name}')
        except RequestTimeoutError as e:
            logging.error(f'RequestTimeoutError: {str(e)}')
            print(f'RequestTimeoutError for item_name: {item_name}')


for historical_data in query_api_generator(extract_item_name_from_table(query_string, DATABASE_NAME)):
    historical_data_df = pd.DataFrame.from_dict(historical_data)
    historical_data_df.head()
