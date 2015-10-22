from lytebot.bot import lytebot
import logging

admin_usernames = ['stevenyo', 'NULLSPHERE']

@lytebot.command('disabled')
def disabled(args):
    disabled = [func.__name__ for func in lytebot.disabled]
    return ', '.join(disabled) if disabled else 'I got nothing!'

@lytebot.command('disable')
def disable(args):
    n = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in admin_usernames:
        return '@{} You can\'t do that'.format(user)

    for s in args.text.split(' ')[1::]:
        if s == 'enable':
            return 'Nah'
        command = lytebot.get_command(s)
        if not command:
            return 'Command {} not found'.format(s)

        if command not in lytebot.disabled:
            n.append(command)
            lytebot.disabled.append(command)
            logging.info('Command \'{}\' disabled by {}'.format(command.__name__, user))
    if len(n) > 0:
        return '@{} Disabled: {}'.format(user, ', '.join([i.__name__ for i in n]))
    else:
        return '@{} Did nothing. Command already disabled.'.format(user)

@lytebot.command('enable')
def enable(args):
    n = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in admin_usernames:
        return '@{} You can\'t do that'.format(user)

    for s in args.text.split(' ')[1::]:
        command = lytebot.get_command(s)
        if not command:
            return '@{} Command {} not found'.format(user, s)

        if command in lytebot.disabled:
            n.append(command)
            lytebot.disabled.remove(command)
            logging.info('Command \'{}\' enabled by {}'.format(command.__name__, user))
    if len(n) > 0:
        return '@{} Enabled {}'.format(user, ', '.join([i.__name__ for i in n]))
    else:
        return '@{} Did nothing. Command already enabled.'.format(user)

@lytebot.command('ignored')
def ignored(args):
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if not args.chat_id in lytebot.ignore:
        return '@{} Ignoring no-one'.format(user)
    return '@{} Ignoring {}'.format(user, ', '.join(lytebot.ignore[args.chat_id]))

@lytebot.command('ignore')
def ignore(args):
    users = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in admin_usernames:
        return '@{} You can\'t do that'.format(user)

    for u in args.text.split(' ')[1::]:
        u = u.replace('@', '')
        lytebot.set_ignore(args.chat_id, u)
        users.append(u)

    if users:
        return '@{} Ignored {}'.format(user, ', '.join(users))
    else:
        return '@{} Did nothing!'.format(user)

@lytebot.command('unignore')
def unignore(args):
    users = []
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    if args.from_user.username not in admin_usernames:
        return '@{} You can\'t do that'.format(user)

    for u in args.text.split(' ')[1::]:
        u = u.replace('@', '')
        try:
            lytebot.ignore[args.chat_id].remove(u)
        except Exception:
            return "@{} User {} isn't being ignored".format(user, u)
        users.append(u)

    if users:
        return '@{} Unignored {}'.format(user, ', '.join(users))
    else:
        return '@{} Did nothing!'.format(user)
