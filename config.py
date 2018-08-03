import os
import redis


DATE_DELTA = 30

REPO_PARAMS = {
        'client_id': os.environ.get('client_id'),
        'client_secret':  os.environ.get('client_secret'),
    }


REPO_PULL_PARAMS = {
        'client_id': os.environ.get('client_id'),
        'client_secret':  os.environ.get('client_secret'),
        'state': 'all',
    }

REDIS_STORAGE = redis.Redis(host='localhost', port=6379, db=0)