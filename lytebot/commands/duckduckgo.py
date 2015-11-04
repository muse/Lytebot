from lytebot.bot import lytebot
from lytebot.models import duckduckgo
import logging

@lytebot.command('ddg')
def ddg(args, user):
    arg = ''.join(args.text.split(' ')[1::])

    if not arg:
        return '@{} I can\'t hear you -- I\'m using the scrambler.'.format(user)

    return '@{} {}'.format(user, duckduckgo.search(arg))

@lytebot.command('!\w*')
def bang(args, user):
    bang = args.text.split(' ')[0][1::]
    query = ' '.join(args.text.split(' ')[1::])

    return '@{} {}'.format(user, duckduckgo.bang_search(bang, query))
