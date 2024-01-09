import threading

import uvicorn
from fastapi import FastAPI

from rs3_trading.tasks.tasks import update_database_asynchronously
from rs3_trading.utils.url_utils import RS3UrlBuilder, RSDataType
from rs3_trading.utils.utilities import create_database_tables

app = FastAPI()

url_builder = RS3UrlBuilder()
url_price = url_builder(RSDataType.Prices)
url_volume = url_builder(RSDataType.Volumes)

create_database_tables()

if __name__ == "__main__":

    database_thread = threading.Thread(target=update_database_asynchronously, kwargs={'url_price': url_price, 'url_volume': url_volume, 'update_delay': 1800})
    database_thread.start()

    uvicorn.run("main:app", reload=True)
