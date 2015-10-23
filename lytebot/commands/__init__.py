import logging
from lytebot.errors import CommandsDisabled

commands = ['misc', 'duckduckgo', 'imgur', 'admin']

for command in commands:
    module = 'lytebot.commands.{}'.format(command)
    try:
        lib = __import__(module, globals(), locals(), ['*'])
    except CommandsDisabled as e:
        logging.warning(e)
    else:
        globals()[command] = lib
