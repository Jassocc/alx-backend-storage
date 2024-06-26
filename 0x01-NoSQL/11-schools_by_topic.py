#!/usr/bin/env python3
"""
script for task 11
"""


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
                },
            },
        }
    return [do for do in mongo_collection.find(topic_filter)]
