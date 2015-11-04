from lytebot.errors import CommandsDisabled
from lytebot.bot import lytebot, config
import logging

if 'owners' not in config['telegram']:
    raise CommandsDisabled('There is no owner set in your Lytebot config. Admin commands are disabled.')

@lytebot.command('disabled')
def disabled(args, user):
    return ', '.join(lytebot.disabled) if lytebot.disabled else 'I got nothing!'

@lytebot.command('disable', admin=True)
def disable(args, user):
    n = []

    for s in args.text.split(' ')[1::]:
        if s == 'enable':
            return '@{} Nah'.format(user)
        try:
            command = lytebot.get_command(s)['func']
        except IndexError:
            return '@{} Command {} not found'.format(user, s)

        if command not in lytebot.disabled:
            n.append(command)
            lytebot.disable(command.__name__)
            logging.info('Command \'{}\' disabled by {}'.format(command.__name__, user))
    if n:
        return '@{} Disabled: {}'.format(user, ', '.join([i.__name__ for i in n]))
    else:
        return '@{} Did nothing. Command already disabled.'.format(user)

@lytebot.command('enable', admin=True)
def enable(args, user):
    n = []

    for s in args.text.split(' ')[1::]:
        try:
            command = lytebot.get_command(s)['func']
        except IndexError:
            return '@{} Command {} not found'.format(user, s)

        if command.__name__ in lytebot.disabled:
            n.append(command.__name__)
            lytebot.enable(command.__name__)
            logging.info('Command \'{}\' enabled by {}'.format(command.__name__, user))
    if n:
        return '@{} Enabled {}'.format(user, ', '.join(n))
    else:
        return '@{} Did nothing. Command already enabled.'.format(user)

@lytebot.command('ignored')
def ignored(args, user):
    if not args.chat_id in lytebot.ignored:
        return '@{} Ignoring no-one'.format(user)
    return '@{} Ignoring {}'.format(user, ', '.join(lytebot.ignored[args.chat_id]))

@lytebot.command('ignore', admin=True)
def ignore(args, user):
    users = []

    for u in args.text.split(' ')[1::]:
        lytebot.ignore(args.chat_id, u)
        users.append(u)

    if users:
        return '@{} Ignored {}'.format(user, ', '.join(users))
    else:
        return '@{} Did nothing!'.format(user)

@lytebot.command('unignore', admin=True)
def unignore(args, user):
    users = []

    for u in args.text.split(' ')[1::]:
        try:
            lytebot.unignore(args.chat_id, u)
            users.append(u)
        except Exception:
            return "@{} User {} isn't being ignored".format(user, u)

    if users:
        return '@{} Unignored {}'.format(user, ', '.join(users))
    else:
        return '@{} Did nothing!'.format(user)

@lytebot.command('blacklist', admin=True)
def blacklist(args):
    subs = []

    for s in args.text.split(' ')[1::]:
        lytebot.blacklist(s)
        subs.append(s)

    if subs:
        logging.info('Sub(s) \'{}\' blacklisted by {}'.format(', '.join(subs), user))
        return '@{} Blacklisted {}'.format(user, ', '.join(subs))
    else:
        return '@{} Did nothing!'.format(user)
