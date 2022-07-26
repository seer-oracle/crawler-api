# -*- coding: utf-8 -*-

from src.config import DefaultConfig
from rediscluster import RedisCluster
from src.utils import dex


# File: extensions.py
# Created at 04/05/2022
"""
   Description:
        -
        -
"""

    
assets = [
          'VETUSDT','VEUSDUSDT','VTHOUSDT','BTCUSDT','ETHUSDT','USDT','BUSDUSDT', 'VEXUSDT', 'WVETUSDT',
          'VETBUSD','VEUSD','VTHOBUSD','BTCBUSD','ETHBUSD','BUSD'
          'VETUSD','VEUSDUSD','VTHOUSD','BTCUSD','ETHUSD','USD','BUSDUSD', 'VEXUSD', 'WVETUSD',
          'BTC', 'ETH', 'VEUSD', 'VET', 'VTHO','VEX','WVET'
          ]

ws_dex_list = [
    {   
        "name": "BitMart",
        "url": "wss://ws-manager-compress.bitmart.com/api?protocol=1.1",
        "message":'{"op": "subscribe", "args": ["spot/ticker:BTC_USDT", "spot/ticker:ETH_USDT",  "spot/ticker:VET_USDT", "spot/ticker:VTHO_USDT", "spot/ticker:BUSD_USDT"]}'
        
    },
]

dex_list = [
            {   
                "name": "Gemini",
                "url": "https://www.gemini.com/api/all-prices/5s",
                "delay": 5 #seconds
            },
            {   
                "name": "Binance",
                "url": "https://www.binance.com/bapi/composite/v1/public/marketing/symbol/list",
                "delay": 3 #seconds
            }
            ,
            {   
                "name": "Binance_CW",
                "url": "https://billboard.service.cryptowat.ch/markets?page=1&limit=3000&volumeInAssets=usd&sort=price&sortAsset=usd&onlyExchanges=binance",
                "delay": 5 #seconds
            },
            {   
                "name": "Kraken_CW",
                "url": "https://billboard.service.cryptowat.ch/markets?page=1&limit=3000&volumeInAssets=usd&sort=price&sortAsset=usd&onlyExchanges=kraken",
                "delay": 5 #seconds
            },
            {   
                "name": "CoinBase",
                "url": "https://www.coinbase.com/api/v2/assets/search?filter=listed&include_prices=true&limit=3000&order=asc&page=1&resolution=day&sort=rank",
                "delay": 5 #seconds
            },
            {   
                "name": "Kraken",
                "url": "https://www.kraken.com/api/internal/cryptowatch/markets/assets?asset=USD&limit=3000&assetName=new",
                "delay": 5 #seconds
            },
            {   
                "name": "Vexchange",
                "url": "https://api.vexchange.io/v1/pairs",
                "delay": 5 #seconds
            },
            {   
                "name": "Poloniex",
                "url": "https://poloniex.com/public?command=returnTicker",
                "delay": 5 #seconds
            },
            {   
                "name": "KuCoin",
                "url": "https://www.kucoin.com/_api/quicksilver/universe-currency/market/currency-list?lang=en_US",
                "delay": 5 #seconds
            },
            {   
                "name": "OceanEx",
                "url": "https://engine.oceanex.pro/api/v2/tickers",
                "delay": 5 #seconds
            },
            {   
                "name": "Houbi",
                "url": "https://billboard.service.cryptowat.ch/markets?page=1&limit=3000&volumeInAssets=usd&sort=price&sortAsset=usd&onlyExchanges=huobi",
                "delay": 5 #seconds
            },
           
        ]

class Extensions(object):
   
    
    redis_cluster = RedisCluster(startup_nodes=DefaultConfig.REDIS_CLUSTER,
                                     decode_responses=True, skip_full_coverage_check=True)
       
    def filter_price_by_dex(dex_name, price_respone):
        _prices = []
    
        if dex_name == 'Kraken_CW' or dex_name == 'Binance_CW' or dex_name == 'Houbi':
            _prices = price_respone.get("result").get("rows")
        
        if dex_name == 'Kraken':
            _prices = price_respone.get("result")
            
        if dex_name == 'Binance' or dex_name == 'CoinBase' \
            or dex_name == 'KuCoin':
            _prices = price_respone.get("data")    
            
        if dex_name == 'Gemini':
            _prices = price_respone.get("prices")   
        
        if dex_name == 'Vexchange':
            _prices = dex.convert_to_vexchange_array(price_respone)  
            
        if dex_name == 'Poloniex':
            _prices = dex.convert_to_poloniex_array(price_respone)         
        
        if dex_name == 'OceanEx':
            _prices = dex.convert_to_oceanex_array(price_respone)             

        return _prices 


    def filter_data_by_dex(dex_name, price):
        _symbol = ""
        _price = 0
        if dex_name == 'Kraken_CW' or dex_name == 'Binance_CW' or dex_name == 'Houbi':
            _symbol = price.get("instrument")
            _price = price.get("summary").get("price").get("last")
            
        if dex_name == 'Kraken':
            _symbol = price.get("asset")
            _price = price.get("price")
            
        if dex_name == 'CoinBase':
            _symbol = f'{price.get("symbol")}USD'
            _price = price.get("latest")    
                
        if dex_name == 'Binance':
            _symbol = price.get("symbol")
            _price = price.get("price")    
            
        if dex_name == 'Gemini':
            _symbol = price.get("symbol")
            _price = price.get("bid")     
        
        if dex_name == 'Vexchange':
            _symbol =  f'{price.get("symbol")}'
            _price = price.get("token0").get("usdPrice")
            
        if dex_name == 'Poloniex':
            _symbol =  f'{price.get("symbol")}'
            _price = price.get("last")
            
        if dex_name == 'KuCoin':
            _symbol = price.get("symbol").replace("-", "")
            _price = price.get("lastPrice")   
            
        if dex_name == 'OceanEx':
            _symbol = price.get("symbol")
            _price = price.get("last")       
            
        if not _symbol:
            return None
        
        for asset in assets:  
            if asset == _symbol.upper():    
                _dex_result = {
                    "symbol": _symbol.upper(),
                    "price": _price
                }
                return _dex_result
            
        return None     
          
   
