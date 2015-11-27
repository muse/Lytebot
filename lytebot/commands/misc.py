from lytebot.bot import lytebot

@lytebot.command('start')
def start(args, user):
    return '''Hi! I'm a multifunctional, convenient and fun bot. I can do all these things:\n
/r [sub]: Random image by subreddit
/ddg [query]: Search DuckDuckGo
/fip: (╯°□°)╯︵ ┻━┻
/back: ┬─┬ ノ( ゜-゜ノ)
/disabled: Show disabled commands
/![bang] [query]: Search DuckDuckGo by bang


/disable [command]: Disable a command
/enable [command]: Enable a command
/ignore [user]: Ignore a user (don't execute commands sent by user)
/unignore [user]: Unignore a user
/blacklist [sub]: Blacklist subreddit from /r command
/whitelist [sub]: Whitelist subreddit from /r command
'''

@lytebot.command('!!')
def repeat(args, user):
    chat_id = args.chat_id

    try:
        lytebot.previous[chat_id]['args'].from_user = args.from_user
        return lytebot.previous[chat_id]['func'](lytebot.previous[chat_id]['args'], user)
    except KeyError:
        return '@{} I got nuthing!'.format(user)

@lytebot.command('hey')
def hey(args, user):
    return 'Hi!'

@lytebot.command('flip')
def flip(args, user):
    return '(╯°□°)╯︵ ┻━┻'

@lytebot.command('back')
def back(args, user):
    return '┬─┬ ノ( ゜-゜ノ)'
