import os
import re
import sys
import logging
import telegram
import lytebot
import lytebot.models

from lytebot import config, config_dir

# set up logging
log_format = '%(asctime)s [%(levelname)-5.5s] %(message)s'
logging.basicConfig(filename='{}/lytebot.log'.format(config_dir),
                    format=log_format, level=logging.INFO)

# stdout logger
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(log_format))

logging.getLogger('').addHandler(console)

class Bot:
    _last_id = None
    ignore = {}
    commands = {}
    disabled = []
    previous = {}

    def __init__(self, prefix='/'):
        self.prefix = prefix

    def _set_previous(self, func, args):
        '''
        Save previous command per chat

        :param func: Command function
        :param args: Arguments given to command
        '''
        self.previous[args.chat_id] = {'func': func, 'args': args}

    def set_ignore(self, chat_id, user):
        '''
        Ignore a user in a chat

        :param chat_id: Chat ID
        :param user: Username to ignore
        '''
        if not chat_id in self.ignore:
            self.ignore[chat_id] = []
        if not user in self.ignore[chat_id]:
            self.ignore[chat_id].append(user)

    def command(self, handle):
        '''
        Create a new command entry, saved in self.commands

        :param handle: The name for the command
        :returns: Function
        '''
        def arguments(function):
            if type(function).__name__ == 'function':
                self.commands[handle] = function
            else:
                logging.warning('{}.{} -> {}'.format(self.__class__.__name__, '__name__',
                         'Detected argument was not a function'))
            logging.info('Found command -> {}'.format(function.__name__))
            return self.commands
        return arguments

    def get_command(self, message):
        '''
        Gets command from message sent, if it contains a command

        :param message: Message that could contain a command
        :returns: Function or False
        '''
        for command in self.commands:
            if re.match(r'^({0}$|{0}\ \w*)'.format(command), message):
                return self.commands[command]

        return False

    def run(self):
        '''Start listening for commands'''
        bot = telegram.Bot(token=config['telegram']['token'])
        # Disable Telegram API's logger to prevent spam
        bot.logger.disabled = True

        logging.info('Started bot')

        # TODO: Make this not hacky with tries.
        try:
            self._last_id = bot.getUpdates()[-1].update_id
        except IndexError:
            self._last_id = None
        except telegram.error.TelegramError as e:
            logging.critical('Failed to start bot: {} (is your Telegram token correct?)'.format(e))
            sys.exit(1)

        try:
            while True:
                for update in bot.getUpdates(offset=self._last_id, timeout=10):
                    if not update.message['text']:
                        continue

                    if update.message.chat_id in self.ignore and \
                       update.message.from_user.username in self.ignore[update.message.chat_id]:
                        continue

                    message = update.message.text[1::]
                    prefix = update.message.text[0]
                    command = self.get_command(message)

                    if command and prefix == self.prefix and command not in self.disabled:
                        bot.sendMessage(
                            chat_id=update.message.chat_id,
                            text=command(update.message)
                        )
                        self._last_id = update.update_id + 1

                        if not message.startswith('!!'):
                            self._set_previous(command, update.message)
        except KeyboardInterrupt:
            logging.info('Stopped bot')

lytebot = Bot()
