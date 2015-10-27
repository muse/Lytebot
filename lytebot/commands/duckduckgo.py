from lytebot.bot import lytebot
from lytebot.models import duckduckgo
import logging

@lytebot.command('ddg')
def ddg(args):
    arg = ''.join(args.text.split(' ')[1::])
    user = args.from_user.username if args.from_user.username else args.from_user.first_name

    if not arg:
        return '@{} I can\'t hear you -- I\'m using the scrambler.'.format(user)

    return '@{} {}'.format(user, duckduckgo.search(arg))

@lytebot.command('!\w*')
def bang(args):
    bang = args.text.split(' ')[0][1::]
    query = ' '.join(args.text.split(' ')[1::])

    return duckduckgo.bang_search(bang, query)
