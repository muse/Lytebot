import logging
import random
import re
import imgurpython as imgur
from lytebot import config
from lytebot.bot import lytebot

# thanks mvdw and techwolf12
sub_blacklist = ['traps', 'spacedicks', '^porn$', 'submissive', 'nsfw', 'gonewild',
                 'boob', 'yiff', 'furry']

try:
    imgur_client = imgur.ImgurClient(config['imgur']['id'], config['imgur']['secret'])
except KeyError as e:
    logging.error('Missing imgur[{}] in configuration file. Disabling imgur commands'.format(e) +
                  ' (see config.json.example for an example)')
except imgur.helpers.error.ImgurClientError as e:
    logging.error(e)
    logging.warning('Imgur commands won\'t work. This should resolve itself over time')

@lytebot.command('r')
def r(args):
    arg = args.text.split(' ')[1] if len(args.text.split(' ')) > 1 else 'all'
    user = args.from_user.username if args.from_user.username else args.from_user.first_name

    random_sort = random.choice(['time', 'top'])

    for i in sub_blacklist:
        if re.search(i, arg):
            return '@{} You speak an infinite deal of nothing'.format(user)

    try:
        items = imgur_client.subreddit_gallery(arg, sort=random_sort, window='year', page=0)
    except Exception as e:
        logging.warning('ImgurClient: {}'.format(e))
        return '@{} I can\'t help you at this time. Try again later.'.format(user)

    if not items:
        return '@{} My pet ferret can type better than you!'.format(user)

    return '@{} {}'.format(user, random.choice(items).link)

@lytebot.command('kaf')
def kaf(args):
    random_sort = random.choice(['time', 'top'])
    user = args.from_user.username if args.from_user.username else args.from_user.first_name
    try:
        items = imgur_client.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)
    except Exception as e:
        logging.warning('ImgurClient: {}'.format(e))
        return '@{} I can\'t help you at this time. Try again later.'.format(user)

    return '@{} {}'.format(user, random.choice(items).link)
