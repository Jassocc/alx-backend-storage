#!/usr/bin/env python3
"""
script for taS K14
"""


def top_students(mongo_collection):
    """
    prints average scores of childfren
    """
    studs = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return studs
