# -*- coding: utf-8 -*-

# File: stream.py	
# Created at 04/04/2022
import json
import traceback
from datetime import datetime

import bcrypt

import requests
from src.config import DefaultConfig


class PriceHelper(object):
    
    @staticmethod
    def get_pricing(url_request: str()):
        
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.request(
                                    method="GET", 
                                    url=url_request,
                                    headers=headers
                                    )
            if  response.status_code == 200:
                data = response.json()
                return data

        except Exception as e:
            traceback.print_exc(e)

        return None
    
    