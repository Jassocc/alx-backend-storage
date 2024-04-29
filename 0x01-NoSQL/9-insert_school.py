#!/usr/bin/env python3
"""
script for task 9
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a file in the db
    """
    file_ins = mongo_collection.insert_one(kwargs)
    return file_ins.inserted_id
