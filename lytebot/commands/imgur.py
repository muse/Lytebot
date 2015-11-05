import logging
import random
import re
import imgurpython as imgur
from lytebot.errors import CommandsDisabled
from lytebot import config
from lytebot.bot import lytebot

try:
    imgur_client = imgur.ImgurClient(config['imgur']['id'], config['imgur']['secret'])
except KeyError as e:
    raise CommandsDisabled('Missing imgur[{}] in configuration file. Disabling imgur commands'.format(e) +
                           ' (see config.example.yml for an example)')
except Exception as e:
    raise CommandsDisabled(e)
except imgur.helpers.error.ImgurClientError as e:
    logging.error(e)
    raise CommandsDisabled('Imgur commands disabled. This should resolve itself over time')

@lytebot.command('r')
def r(args, user):
    arg = args.text.split(' ')[1] if len(args.text.split(' ')) > 1 else 'all'

    random_sort = random.choice(['time', 'top'])

    for i in lytebot.blacklisted:
        if re.search(i.lower(), arg.lower()):
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
def kaf(args, user):
    random_sort = random.choice(['time', 'top'])

    try:
        items = imgur_client.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)
    except Exception as e:
        logging.warning('ImgurClient: {}'.format(e))
        return '@{} I can\'t help you at this time. Try again later.'.format(user)

    return '@{} {}'.format(user, random.choice(items).link)
