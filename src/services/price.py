import json, hmac, hashlib, time, base64
import asyncio
import time
import websockets
import sys
from src.helpers.pricing import PriceHelper
from datetime import datetime, timezone
from src.extensions import Extensions, assets, ws_dex_list
from src.worker.price import save_price

async def get_price_socket():
    s = time.gmtime(time.time())
    TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", s)
    for dex in ws_dex_list:
        uri = dex.get("url")
        print("uri ", uri)
        async with websockets.connect(uri, ping_interval=None, max_size=None) as websocket:
            _message =  dex.get("message")
            print("_message ", _message)
            await websocket.send(_message)
            try:
                processor = None
                while True:
                    response = await websocket.recv()
                    _datetime_second = str(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).split(".")[0]                        
                    parsed = json.loads(response)
                    stream = parsed.get("data")
                    if stream:

                        key = f"{_datetime_second}_{dex.get('name')}"
                        for dt in stream:
                            _symbol =  dt.get("symbol").replace("_", "")
                            for asset in assets:   
                                if f'{asset}' ==  _symbol:   
                                    _price_param = {
                                        "symbol": _symbol.upper(),
                                        "price": dt.get("last_price")
                                    }
                                    print(key, _price_param)
                                    
                                    # save price crawl
                                    save_price(_price_param, dex, key)
            except websockets.exceptions.ConnectionClosedError:
                print("Error caught")
                sys.exit(1)
                
                
def get_price_interval(dex_price, key):
    price_response = PriceHelper.get_pricing(dex_price.get("url"))
    if not price_response:
        return None
    
    dex_name =  dex_price.get("name")
    _prices = Extensions.filter_price_by_dex(dex_name, price_response)
    if not _prices:
        return None
    
    for price in _prices:
        dex_result = Extensions.filter_data_by_dex(dex_name, price)
        if dex_result:
            
            # save price crawl
            save_price(dex_result, dex_price, key)

            
                