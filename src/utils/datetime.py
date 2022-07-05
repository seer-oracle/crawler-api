# -*- coding: utf-8 -*-

from datetime import datetime


def get_current_time():
    return datetime.utcnow()


def get_expired_time(start: datetime, time: float):
    return datetime.fromtimestamp(
        start.timestamp() + time
    )
