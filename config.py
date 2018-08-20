import os

DATE_DELTA = 30
CLIENT_ID = os.environ.get('CLIENT_ID')
СLIENT_SECRET = os.environ.get('СLIENT_SECRET')
REPOSITORY = os.environ.get('REPOSITORY')
STATE = 'all'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
MODULES = [
	'requests', 'BeautifulSoup', 'django',
	'Flask', 'redis', 'ModuleFinder',
	'setuptools', 'collections', 'openpyxl',
	'bs4', 'functools',
	'bootstrap', 'html', 'css'
]
INVALID_ERROR = 'Invalid values, please try again'
AUTHORIZE_ERROR = "You aren\'t authorized"