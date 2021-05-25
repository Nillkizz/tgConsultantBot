from os import getenv

BOT_API_TOKEN = getenv('BOT_API_TOKEN')
CHAT_ID = getenv('CHAT_ID')

REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = getenv('REDIS_PORT', '6379')
REDIS_DB = getenv('REDIS_DB', '0')

assert CHAT_ID, 'CHAT_ID environment variable is not defined'
