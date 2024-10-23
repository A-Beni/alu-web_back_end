#!/usr/bin/env python3
'''Task 12: Log stats for Nginx request logs in MongoDB'''

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionError


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.
    
    Parameters:
    - nginx_collection: The MongoDB collection of Nginx logs.
    '''
    log_count = nginx_collection.count_documents({})
    print('{} logs'.format(log_count))
    
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, req_count))
    
    # Count GET requests for /status path
    status_checks_count = nginx_collection.count_documents(
        {'method': 'GET', 'path': '/status'}
    )
    print('{} status check'.format(status_checks_count))


def run():
    '''Connect to MongoDB, print Nginx logs stats, and handle connection issues.'''
    
    # Ensure the file exists
    if not os.path.exists(__file__):
        print("File not found.")
        return
    
    # Start MongoDB connection
    try:
        client = MongoClient('mongodb://127.0.0.1:27017')
        db = client.logs
        nginx_collection = db.nginx
        print_nginx_request_logs(nginx_collection)
    except ConnectionError:
        print("Failed to connect to MongoDB. Make sure MongoDB is running.")
        return


if __name__ == '__main__':
    run()

