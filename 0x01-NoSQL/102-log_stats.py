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
    print('Methods')
    metho = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in metho:
        req_c = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_c))
    stat_check = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(stat_check))


def print_ips(server_collection):
    """
    print stats about 10 https
    """
    print('IPs:')
    req_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for req_logging in req_logs:
        ip = req_logging['_id']
        ip_count = req_logging['totalRequests']
        print('\t{}: {}'.format(ip, ip_count))


def run():
    """
    gives some stats
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_request_logs(client.logs.nginx)
    print_ips(client.logs.nginx)


if __name__ == '__main__':
    run()
