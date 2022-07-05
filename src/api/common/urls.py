# -*- coding: utf-8 -*-



# File: urls.py
# Created at 03/04/2022
"""
   Description:
        -
        -
"""

from flask import Blueprint

from src.api.common.controller import health_check

rest_service = Blueprint('rest_service', __name__, url_prefix='common')

rest_service.add_url_rule('health_check', methods=['GET'], view_func=health_check)
