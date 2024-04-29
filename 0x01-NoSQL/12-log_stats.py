#!/usr/bin/env python3
"""
task 12 script
"""
from pymongo import MongoClient


def print_request_logs(nginx_collection):
    """
    prints nginx logs
    """
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    metho = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in metho:
        req_c = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_c))
    stat_check = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(stat_check))


def run():
    """
    gives some stats
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
