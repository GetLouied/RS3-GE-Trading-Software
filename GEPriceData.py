import duckdb
import pandas as pd
import requests

### This section is about getting the data from the url it should be in a function
url = "https://runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"
r = requests.get(url)
data = r.json()

# This should be in a function specific to handling times from the data
unix_time = data.pop('%LAST_UPDATE%')
data.pop('%LAST_UPDATE_F%')

## THis should be in a dataframe transformation function
column_names = ['item_name', 'price']
ge = pd.DataFrame.from_dict(data, orient='index').reset_index()
ge.columns = column_names
ge['time'] = pd.to_datetime(unix_time, unit='s')
ge['item'] = ge['item_name'].str.lower().replace('[^A-Za-z0-9+()]+', '', regex=True)


# Duckdb shit should be in it's own module, but a function for now is fine
con = duckdb.connect('GETest')
con.execute('create table if not exists ge_tick_data(time datetime, item varchar, item_name varchar, price long)')
con.execute("""insert into ge_tick_data(time, item, item_name, price)
            select
                time,
                item,
                item_name,
                price
            from ge""")


## General Stuff
# 1. Spend 5 minutes coming up with decent function names
# 2. use snake_case() for methods
# 3. Create a main.py that calls these functions in the right order
