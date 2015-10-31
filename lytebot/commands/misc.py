from lytebot.bot import lytebot

@lytebot.command('start')
def start(args):
    # This needs working on, telegram automatically issues this command when
    # you talk to the bot for the first time.
    return 'This bot searches Imgur and DuckDuckGo. It also has some other fun usages.'

@lytebot.command('!!')
def repeat(args):
    chat_id = args.chat_id

    try:
        lytebot.previous[chat_id]['args'].from_user = args.from_user
        return lytebot.previous[chat_id]['func'](lytebot.previous[chat_id]['args'])
    except KeyError:
        return 'I got nuthing!'

@lytebot.command('hey')
def hey(args):
    return 'Hi!'

@lytebot.command('flip')
def flip(args):
    return '(╯°□°)╯︵ ┻━┻'

@lytebot.command('back')
def back(args):
    return '┬─┬ ノ( ゜-゜ノ)'
