# -*- coding: utf-8 -*-

# File: merchant.py
# Created at 11/11/2021
"""
   Description:
        -
        -
"""
from pymodm import fields

from lib.model import BaseMG


class PriceModel(BaseMG):
    class Meta:
        collection_name = 'seer_price_raw'
        final = True
        ignore_unknown_fields = True
        
    source = fields.CharField(required=True, blank=False)
    url_source = fields.CharField(required=True, blank=False)
    timestamp = fields.CharField(required=True, blank=False)
    symbol = fields.CharField(required=True, blank=False)
    price = fields.FloatField(required=True, blank=False)
