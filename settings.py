from os import getenv

BOT_API_TOKEN = getenv('BOT_API_TOKEN')
CHAT_ID = getenv('CHAT_ID')


required_params = ['BOT_API_TOKEN', 'CHAT_ID']
for param in required_params:
    assert globals().get(param) is not None, f'{param} cannot be None.'
