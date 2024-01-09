from fastapi.routing import APIRouter
from rs3_trading.contextmanager.contextmanager import DuckDBCM
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/item')


@router.get('/all')
def get_all_items():
    with DuckDBCM('GE_Tick_Data.db') as con:
        df = con.execute('''select distinct item_name
                    from rs3_price_data''').df()
        
        item_names = df['item_name'].tolist()
        json_items_content = {'item_name': item_names}

        
        return JSONResponse(content=json_items_content)