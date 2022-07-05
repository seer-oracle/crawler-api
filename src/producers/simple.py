# -*- coding: utf-8 -*-


# File: pos.py
# Created at 11/11/2021
"""
   Description: 
        -
        -
"""
from lib.exceptions import handle_exception
from lib.worker import send_worker

"""
    
    Format message:
    
    Topic: "test"
        
        {
            "action": PUT, POST, DELETE
            "value": object
        }
        
        - PUT = Update something
        - POST = Request or submit something
        - DELETE = Remove or delete something
"""


@handle_exception()
def send_task(topic, data):
    send_worker(topic, {
        'action': "POST",
        "value": data
    })
