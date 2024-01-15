from fastapi.routing import APIRouter
from rs3_trading.contextmanager.contextmanager import DuckDBCM
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/item')

@router.get('/all')
def get_all_items():
    with DuckDBCM('GE_Tick_Data.db') as con:
        df = con.execute('''
                         select 
                            distinct item_name,
                            item as normalized_item_name
                        from rs3_price_data''').df()
        
        return JSONResponse(content=df.to_dict(orient='records'))
    

@router.get('/{item_name}')
def get_item_data(item_name):
    with DuckDBCM('GE_Tick_Data.db') as con:
        df = con.execute(f"""
                    with dedupped_item_prices as
                    (
                         select 
                            item, 
                            updated_date, 
                            avg(price) as price
                        from rs3_price_data
                        group by item, updated_date
                    ),
                    dedupped_item_volumes as 
                    (
                        select 
                            item, 
                            updated_date, 
                            avg(volume) as volume
                        from rs3_volume_data 
                        group by item, updated_date
                    )
                    
                    select 
                         p.item, 
                         p.updated_date, 
                         p.price, 
                         v.volume
                    from dedupped_item_prices as p
                    inner join dedupped_item_volumes as v on 
                         p.item = v.item and 
                         p.updated_date = v.updated_date
                    where p.item = '{item_name}' 
                    """).df() 
        df['updated_date'] = df['updated_date'].dt.strftime('%Y-%m-%d')
  

        return JSONResponse(content=df.to_dict(orient='records'))
