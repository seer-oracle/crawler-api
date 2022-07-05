# -*- coding: utf-8 -*-


# File: validators.py
# Created at 03/04/2022
"""
   Description:
        -
        -
"""

from bson import ObjectId

from lib.exceptions import handle_exception


@handle_exception(tracking=False, default=False)
def is_oid(oid):
    return ObjectId.is_valid(oid)
