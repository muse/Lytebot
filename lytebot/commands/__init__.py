import logging
from lytebot.errors import CommandsDisabled

try:
    from .misc import *
    from .imgur import *
    from .admin import *
    from .duckduckgo import *
except CommandsDisabled as e:
    logging.warning(e)
