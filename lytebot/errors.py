class CommandsDisabled(Exception):
    '''Raised when commands can't be loaded for some reason and get disabled'''
    pass

class CommandError(Exception):
    '''Raised when something went wrong trying to access a command'''
    pass
