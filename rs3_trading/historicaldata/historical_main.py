from rs3_trading.database.dbcm import DuckDBCM

DATABASE_NAME = 'GE_Tick_Data.db'
column_name = 'item_name'

query = f'SELECT {column_name} FROM rs3_price_data'

with DuckDBCM(file_name=DATABASE_NAME) as con:
    con.execute(query)
    results = con.fetchall()
    item_names = [row[0] for row in results]

    print(item_names)
