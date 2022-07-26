# -*- coding: utf-8 -*-


# File: dex.py
# Created at 04/05/2022
"""
   Description:
        -
        -
"""

list_address_vexchange = [
    "0x2B6fC877fF5535b50f6C3e068BB436b16EC76fc5",
    "0x25491130A43d43AB0951d66CdF7ddaC7B1dB681b",
    "0xCcdBAA63258AD945Ce4DCfFA4E09C62c9005B092",
    "0x6c33A10d32aC466c324F23A949cC3F4B70AF4513"
]

list_address_poloniex = [
    {
     "key": "USDT_BTC",
     "symbol": "BTCUSDT"
     },
    {
     "key": "USDT_ETH",
     "symbol": "ETHUSDT"
     },
    {
     "key": "USDT_BUSD",
     "symbol": "BUSDUSDT"
     }
]


list_address_oceanex = [
    {
     "key": "VETUSDT",
     "symbol": "VETUSDT"
     },
    {
     "key": "VETVEUSD",
     "symbol": "VETVEUSD"
     },
    {
     "key": "VEUSDUSDT",
     "symbol": "VEUSDUSDT"
     },
    {
     "key": "VTHOUSDT",
     "symbol": "VTHOUSDT"
     },
    {
     "key": "BTCUSDT",
     "symbol": "BTCUSDT"
     },
    {
     "key": "ETHUSDT",
     "symbol": "ETHUSDT"
     },
    {
     "key": "BUSDUSDT",
     "symbol": "BUSDUSDT"
     },
]

def convert_to_vexchange_array(exchange_data):
    vexchange = []
    for address in list_address_vexchange:
        _ex_data = exchange_data.get(address)
        _ex_data['symbol'] = f'{_ex_data.get("token0").get("symbol")}USD'
        vexchange.append(_ex_data)
    return vexchange  

def convert_to_poloniex_array(exchange_data):
    poloniex = []
    for address in list_address_poloniex:
        _ex_data = exchange_data.get(address.get("key"));
        _ex_data['symbol'] = address.get("symbol")
        poloniex.append(_ex_data)
    return poloniex   


def convert_to_oceanex_array(exchange_data):
    oceanex = []
    for address in list_address_oceanex:
        _ex_data = exchange_data.get(address.get("key").lower());
        _ex_data['symbol'] = address.get("symbol")
        oceanex.append(_ex_data)
    return oceanex
