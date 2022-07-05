from src.services.price import get_price_interval
from datetime import datetime, timezone
from src.extensions import dex_list
from lib.logger import logger


class ScheduleService(object):
    
    @staticmethod   
    def get_price():
        
        _datetime_second = str(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).split(".")[0]   
        for dex in dex_list:
    
            key = f"{_datetime_second}_{dex.get('name')}"     
            get_price_interval(dex, key)
           
            
  