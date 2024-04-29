#!/usr/bin/env python3
"""
script for task 8
"""


def list_all(mongo_collection):
    """
    lists all doc's in db
    """
    return [do for do in mongo_collection.find()]
