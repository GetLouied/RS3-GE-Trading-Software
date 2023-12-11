import duckdb
import uvicorn
from fastapi import FastAPI

from rs3_trading.database.ge_tick_database import create_ge_tick_table, insert_into_tick_table
from rs3_trading.utils.utilities import data_retrieval, pop_unix_time_from_dict, transform_to_tick_dataframe

app = FastAPI()


@app.get('/database')
def create_database():
    url = "https://runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"

    price_data = data_retrieval(url)
    unix_time = pop_unix_time_from_dict(price_data)
    ge_tick_dataframe = transform_to_tick_dataframe(price_data, unix_time)

    con = duckdb.connect('GETest')
    create_ge_tick_table(con)
    insert_into_tick_table(con, ge_tick_dataframe)
    return ("Successful")


if __name__ == "__main__":
    uvicorn.run("main:app")
