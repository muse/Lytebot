from lytebot.bot import lytebot
import random

@lytebot.command('start')
def start(args, user):
    return '''Hi! I'm a multifunctional, convenient and fun bot. I can do all these things:\n
/r [sub]: Random image by subreddit
/ddg [query]: Search DuckDuckGo
/flip: (╯°□°)╯︵ ┻━┻
/back: ┬─┬ ノ( ゜-゜ノ)
/shruggie: ¯\_(ツ)_/¯
/disabled: Show disabled commands
/![bang] [query]: Search DuckDuckGo by bang
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
    greetings = ['Hey @{}, hope you are having a wonderful day!', 'Hi @{}, how are you doing?', 'Hello @{}']
    return random.choice(greetings).format(user)

@lytebot.command('flip')
def flip(args, user):
    return '(╯°□°)╯︵ ┻━┻'

@lytebot.command('back')
def back(args, user):
    return '┬─┬ ノ( ゜-゜ノ)'

@lytebot.command('shruggie')
def shruggie(args, user):
    return '¯\_(ツ)_/¯'

