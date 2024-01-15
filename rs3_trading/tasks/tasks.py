import time

from rs3_trading.utils.utilities import update_database


def update_database_asynchronously(url_price: str, url_volume: str, update_delay: int):
    while True:
        update_database(url_price, url_volume)
        print('database updated')
        time.sleep(update_delay)
        print('sleep complete')
