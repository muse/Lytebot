from lytebot.bot import lytebot
import random
import urbandict as udc

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

@lytebot.command('boes')
def boes(args, user):
  boesString = ''
  for word in args:
    s = list(word)[0] = 'b'
    "".join(s)
    boesString += s+' '
  return '@{} {}'.format(user, boesString)

@lytebot.command('ud')
def ud(ex, user):
  try:
    dict = udc.define(args[1])
  except Exeption as e:
    logging.info('DuckDuckGo: {}'.format(e))
    return '@{} Couldn\'t find that shit man. sry'

  return '@{} \n @{} \n @{}'.format(user, dict[0].def, dict[0].example)

@lytebot.command('bored')
def bored():
    cn = randint(0,99)
    cl = randint(0,87)
    return '@{} program #{} in language #{} from this link : http://imgur.com/a/4MBAI .'.format(user, cn, cl)

@lytebot.command('fittie')
def fittie(args, user):
  return '@{} challanged @{} to a fittie. my bets are on the white boy to the left.'.format(user, args[1])
