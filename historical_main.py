import asyncio

from rs3_trading.historicaldata.historical_process import main

loop = asyncio.get_event_loop()
loop.run_until_complete(main('GE_Tick_Data.db', 5))
