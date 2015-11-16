import logging
import lytebot.errors
from lytebot.bot import lytebot, config

if 'owners' not in config['telegram']:
    raise CommandsDisabled('There is no owner set in your Lytebot config. Admin commands are disabled.')

@lytebot.command('disabled')
def disabled(args, user):
    return '@{} '.format(user) + (', '.join(lytebot.disabled) if lytebot.disabled else 'I got nothing!')

@lytebot.command('disable', admin=True)
def disable(args, user):
    commands = []

    for s in args.text.split(' ')[1::]:
        if s == 'enable':
            return '@{} Nah'.format(user)

        command = lytebot.get_command(s)
        if not command:
            return '@{} Command {} not found'.format(user, s)

        try:
            lytebot.disable(command)
        except CommandError as e:
            return '@{} {}'.format(user, e)
        else:
            commands.append(command['func'].__name__)

    if commands:
        logging.info('Command(s) \'{}\' disabled by {}'.format(''.join(commands), user))
        return '@{} Disabled {}'.format(user, ', '.join(commands))

    return '@{} Did nothing. Command already disabled.'.format(user)

@lytebot.command('enable', admin=True)
def enable(args, user):
    commands = []

    for s in args.text.split(' ')[1::]:
        command = lytebot.get_command(s)
        if not command:
            return '@{} Command {} not found'.format(user, s)

        try:
            lytebot.enable(command)
        except CommandError as e:
            return '@{} {}'.format(user, e)
        else:
            commands.append(command['func'].__name__)

    if commands:
        logging.info('Command(s) \'{}\' enabled by {}'.format(', '.join(commands), user))
        return '@{} Enabled {}'.format(user, ', '.join(commands))

    return '@{} Did nothing. Command(s) already enabled.'.format(user)

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
        logging.info('User(s) \'{}\' ignored by {}'.format(', '.join(users), user))
        return '@{} Ignored {}'.format(user, ', '.join(users))

    return '@{} Did nothing!'.format(user)

@lytebot.command('unignore', admin=True)
def unignore(args, user):
    users = []

    for u in args.text.split(' ')[1::]:
        try:
            lytebot.unignore(args.chat_id, u)
        except Exception:
            return "@{} User {} isn't being ignored".format(user, u)
        else:
            users.append(u)

    if users:
        return '@{} Unignored {}'.format(user, ', '.join(users))

    return '@{} Did nothing!'.format(user)

@lytebot.command('blacklist', admin=True)
def blacklist(args, user):
    subs = []

    for s in args.text.split(' ')[1::]:
        lytebot.blacklist(s)
        subs.append(s)

    if subs:
        logging.info('Sub(s) \'{}\' blacklisted by {}'.format(', '.join(subs), user))
        return '@{} Blacklisted {}'.format(user, ', '.join(subs))

    return '@{} Did nothing!'.format(user)
