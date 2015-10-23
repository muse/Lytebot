from lytebot.errors import CommandsDisabled
from lytebot.bot import lytebot, config
import logging

if not 'owners' in config['telegram']:
    raise CommandsDisabled('There is no owner set in your Lytebot config. Admin commands are disabled.')

@lytebot.command('disabled')
def disabled(args):
    return ', '.join(lytebot.disabled) if lytebot.disabled else 'I got nothing!'

@lytebot.command('disable')
def disable(args):
    n = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in config['telegram']['owners']:
        return '@{} You can\'t do that'.format(user)

    for s in args.text.split(' ')[1::]:
        if s == 'enable':
            return 'Nah'
        command = lytebot.get_command(s)
        if not command:
            return 'Command {} not found'.format(s)

        if command not in lytebot.disabled:
            n.append(command)
            lytebot.disable(command.__name__)
            logging.info('Command \'{}\' disabled by {}'.format(command.__name__, user))
    if n:
        return '@{} Disabled: {}'.format(user, ', '.join([i.__name__ for i in n]))
    else:
        return '@{} Did nothing. Command already disabled.'.format(user)

@lytebot.command('enable')
def enable(args):
    n = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in config['telegram']['owners']:
        return '@{} You can\'t do that'.format(user)

    for s in args.text.split(' ')[1::]:
        command = lytebot.get_command(s)
        if not command:
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
def ignored(args):
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if not args.chat_id in lytebot.ignored:
        return '@{} Ignoring no-one'.format(user)
    return '@{} Ignoring {}'.format(user, ', '.join(lytebot.ignored[args.chat_id]))

@lytebot.command('ignore')
def ignore(args):
    users = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in config['telegram']['owners']:
        return '@{} You can\'t do that'.format(user)

    for u in args.text.split(' ')[1::]:
        u = u.replace('@', '')
        lytebot.ignore(args.chat_id, u)
        users.append(u)

    if users:
        return '@{} Ignored {}'.format(user, ', '.join(users))
    else:
        return '@{} Did nothing!'.format(user)

@lytebot.command('unignore')
def unignore(args):
    users = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in config['telegram']['owners']:
        return '@{} You can\'t do that'.format(user)

    for u in args.text.split(' ')[1::]:
        u = u.replace('@', '')
        try:
            lytebot.unignore(args.chat_id, u)
            users.append(u)
        except Exception:
            return "@{} User {} isn't being ignored".format(user, u)

    if users:
        return '@{} Unignored {}'.format(user, ', '.join(users))
    else:
        return '@{} Did nothing!'.format(user)
