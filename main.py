import duckdb

from database.ge_tick_database import create_ge_tick_table, insert_into_tick_table
from utils.utilities import data_retrieval, time_retrieval, transform_to_tick_dataframe

url = "https://runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"

price_data = data_retrieval(url)

unix_time = time_retrieval(price_data)

ge_tick_dataframe = transform_to_tick_dataframe(price_data, unix_time)

con = duckdb.connect('GETest')

create_ge_tick_table(con)
insert_into_tick_table(con, ge_tick_dataframe)
