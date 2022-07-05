import json, hmac, hashlib, time, base64
import asyncio
import time
import websockets
import sys
from src.helpers.pricing import PriceHelper
from datetime import datetime, timezone
from src.extensions import Extensions
from src.worker.price import save_price

def get_price_interval(dex_price, key):
    price_respone = PriceHelper.get_pricing(dex_price.get("url"))
    if not price_respone:
        return None
    
    dex_name =  dex_price.get("name")
    _prices = Extensions.filter_price_by_dex(dex_name, price_respone)
    if not _prices:
        return None
    
    for price in _prices:
        dex_result = Extensions.filter_data_by_dex(dex_name, price)
        if dex_result:
            save_price(dex_result, dex_price, key)

            
                