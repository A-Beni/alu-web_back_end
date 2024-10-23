#!/usr/bin/env python3
'''
Task 12: Log stats for Nginx request logs stored in MongoDB

This script connects to MongoDB, retrieves log information from the 'nginx' collection, and 
prints various statistics (e.g., request method counts, status checks). It is designed to work 
with collections of varying sizes, including empty, small, or large datasets.
'''

import os
import subprocess
from pymongo import MongoClient
from pymongo.errors import ConnectionError


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.

    Args:
    nginx_collection (Collection): The MongoDB collection of Nginx logs.

    Handles:
    - Empty collection
    - Collection with a varying number of documents
    '''
    # Fetch and print total logs count
    log_count = nginx_collection.count_documents({})
    print(f'{log_count} logs')

    # Handle case when the collection is empty
    if log_count == 0:
        print("Collection is empty. No logs to display.")
        return

    # Print method statistics
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {req_count}')

    # Count GET requests to /status path
    status_checks_count = nginx_collection.count_documents({
        'method': 'GET', 'path': '/status'
    })
    print(f'{status_checks_count} status check')


def stop_mongodb():
    '''Stops the MongoDB service if running. Works for Linux-based systems.

    On Linux, this uses the 'systemctl' command to stop MongoDB. On other systems,
    you may need to adjust this depending on the service management tool.
    '''
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'mongod'], check=True)
        print("MongoDB stopped successfully.")
    except subprocess.CalledProcessError:
        print("Failed to stop MongoDB. Ensure you have administrative privileges and MongoDB is installed.")


def run():
    '''Main function to connect to MongoDB, print stats, and handle connection issues.'''
    
    # Check if the script file exists
    if not os.path.exists(__file__):
        print("Script file not found.")
        return
    
    # Start MongoDB connection
    try:
        client = MongoClient('mongodb://127.0.0.1:27017')
        db = client.logs
        nginx_collection = db.nginx

        # Call the function to print log stats
        print_nginx_request_logs(nginx_collection)

    except ConnectionError:
        print("Failed to connect to MongoDB. Make sure MongoDB is running.")
        return

    # Optionally stop MongoDB
    stop_mongodb()


if __name__ == '__main__':
    run()
