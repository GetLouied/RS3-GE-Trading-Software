def create_price_table(con):
    con.execute('create table if not exists rs3_price_data(time datetime, item varchar, item_name varchar, price long, primary key(item, time))')


def create_volume_table(con):
    con.execute('create table if not exists rs3_volume_data(time datetime, item varchar, item_name varchar, volume long, primary key(item, time))')


def insert_into_price_table(con, ge_tick_dataframe):
    con.execute("""insert into rs3_price_data(time, item, item_name, price)
            select
                time,
                item,
                item_name,
                price
            from ge_tick_dataframe""")


def insert_into_volume_table(con, ge_tick_dataframe):
    con.execute("""insert into rs3_volume_data(time, item, item_name, volume)
            select
                time,
                item,
                item_name,
                volume
            from ge_tick_dataframe""")
