class CommandsDisabled(Exception):
    '''Raised when commands can't be loaded for some reason and get disabled'''
    pass

class CommandNotFound(Exception):
    '''Raised when trying to access a command that doesn't exist'''
    pass

class CommandAlreadyDisabled(Exception):
    '''Raised when a command is already disabled'''
    pass

class CommandNotDisabled(Exception):
    '''Raised when trying to enable a command that isn't disabled'''
    pass
