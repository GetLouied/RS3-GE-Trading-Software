import threading
import time

import uvicorn
from fastapi import FastAPI

from rs3_trading.utils.utilities import create_database, update_database

app = FastAPI()

url_price = "https://runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"
url_volume = "https://runescape.wiki/?title=Module:GEVolumes/data.json&action=raw&ctype=application%2Fjson"


create_database()
## update_database(url_price, url_volume)


if __name__ == "__main__":

    def update_database_task():
        while True:
            update_database(url_price, url_volume)
            print('database updated')
            time.sleep(60)
            print('sleep complete')

    database_thread = threading.Thread(target=update_database_task)
    database_thread.start()

    uvicorn.run("main:app", reload=True)
