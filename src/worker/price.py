# -*- coding: utf-8 -*-

# File: price.py

"""
   Description: 
        -
        -
"""
from bson import ObjectId

from lib.decorators import handle_exception
from src.task import worker
from src.models.price import PriceModel
from src.extensions import Extensions


@worker.task(name='worker.save_price', rate_limit='100/s')
@handle_exception()
def save_price(dex_result: dict, dex_price: dict, key: str):
    prefix_key = "Oracle:price"
    key_symbol = f"{prefix_key}_{dex_result.get('symbol')}_{key}"
    expired_time = 60*60*1 # 1 hour
    redis_cluster = Extensions.redis_cluster
    redis_cluster.setex(key_symbol,expired_time, dex_result.get("price"))
    
    # store pricing on db 
    price =  {
            "source": dex_price.get("name"),
            "url_source": dex_price.get("url"),
            "timestamp": key.split("_")[0],
            "symbol": dex_result.get('symbol'),
            "price": dex_result.get('price'),

    }
    PriceModel.insert(price)
    return
