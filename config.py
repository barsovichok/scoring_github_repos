import os
import redis


DATE_DELTA = 30
CLIENT_ID = os.environ.get('client_id')
СLIENT_SECRET = os.environ.get('client_secret')
STATE = 'all'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


# REPO_PARAMS = {
#         'client_id': os.environ.get('client_id'),
#         'client_secret':  os.environ.get('client_secret'),
#     }


# REPO_PULL_PARAMS = {
#         'client_id': os.environ.get('client_id'),
#         'client_secret':  os.environ.get('client_secret'),
#         'state': 'all',
#     }

# REDIS_STORAGE = redis.Redis(host='localhost', port=6379, db=0)
