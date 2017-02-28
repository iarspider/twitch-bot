from src.config.config import *

commands = {
    '!dice': {
        'limit': 5,
        'argc': '*',
        'return': 'command'
    }  #,
    # '!attack': {
    #     'limit': 5,
    #     'argc': 1,
    #     'return': 'command'
    # }
}

for channel in config['channels']:
    for command in commands:
        commands[command][channel] = {'last_used': 0}
