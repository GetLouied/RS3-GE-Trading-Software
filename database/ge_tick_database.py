import duckdb

con = duckdb.connect('GETest')


def create_ge_tick_table(con):
    con.execute('create table if not exists ge_tick_data(time datetime, item varchar, item_name varchar, price long)')


def insert_into_tick_table(con, data):
    con.execute("""insert into ge_tick_data(time, item, item_name, price)
            select
                time,
                item,
                item_name,
                price
            from ge_tick_dataframe""")
