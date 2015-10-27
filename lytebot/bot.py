import os
import re
import sys
import logging
import telegram
import lytebot
import yaml
import threading

from lytebot import config, config_dir

# set up logging
log_format = '%(asctime)s [%(levelname)-5.5s] %(message)s'
logging.basicConfig(filename=os.path.join(config_dir, 'lytebot.log'),
                    format=log_format, level=logging.INFO)

# stdout logger
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(log_format))

logging.getLogger('').addHandler(console)

class LyteBot:
    _last_id = None
    ignored = {}
    commands = {}
    disabled = []
    previous = {}
    blacklisted = []

    paths = {
        'ignored': os.path.join(config_dir, 'ignored.yml'),
        'disabled': os.path.join(config_dir, 'disabled.yml'),
        'blacklisted': os.path.join(config_dir, 'blacklisted.yml'),
    }

    def __init__(self, prefix='/'):
        self.prefix = prefix
        self._bot = telegram.Bot(token=config['telegram']['token'])
        # Disable Telegram API's logger to prevent spam
        self._bot.logger.disabled = True

        for n, f in self.paths.items():
            try:
                with open(f, 'r') as f:
                    setattr(self, n, yaml.load(f.read()))
            except FileNotFoundError:
                pass
            except Exception as e:
                logging.warning('Couldn\'t load {} data: {}'.format(n, e))
            else:
                logging.info('Loaded {} data'.format(n))

    def _set_previous(self, func, args):
        '''
        Save previous command per chat

        :param func: Command function
        :param args: Arguments given to command
        '''
        self.previous[args.chat_id] = {'func': func, 'args': args}

    def _handle_msg(self, update):
        '''Handles all messages sent in all chats (that the bot can see)'''
        # Ignore stickers, pictures and other non-text messages
        if not update.message['text']:
            return

        # Is the user who sent the message ignored?
        if update.message.chat_id in self.ignored and \
           update.message.from_user.username in self.ignored[update.message.chat_id]:
            return

        message = update.message.text[1::]
        prefix = update.message.text[0]
        command = self.get_command(message)

        if command and prefix == self.prefix and command.__name__ not in self.disabled:
            t = threading.Thread(target=self._bot.sendMessage, kwargs={
                'chat_id': update.message.chat_id,
                'text': command(update.message)
            })
            t.start()

            self._last_id = update.update_id + 1

            if not message.startswith('!!'):
                self._set_previous(command, update.message)

    def disable(self, command):
        '''Disables a command in _all_ chats'''
        self.disabled.append(command)
        self.save_data(self.paths['disabled'], self.disabled)

    def enable(self, command):
        '''Enables a command in _all_ chats'''
        self.disabled.remove(command)
        self.save_data(self.paths['disabled'], self.disabled)

    def save_data(self, file, data):
        '''
        Saves data to file to persist data even on shutdown

        :param file: File to write to
        :param data: Data to write to file
        '''
        try:
            with open(file, 'w') as f:
                f.write(yaml.dump(data))
        except Exception as e:
            logging.warning('Failed to save data: {}'.format(e))

    def ignore(self, chat_id, user):
        '''
        Ignores a user in a chat

        :param chat_id: Chat ID
        :param user: Username to ignored
        '''
        if not chat_id in self.ignored:
            self.ignored[chat_id] = []
        if not user in self.ignored[chat_id]:
            # allow /ignore @username for convenience
            user = user.replace('@', '')
            self.ignored[chat_id].append(user)

        self.save_data(self.paths['ignored'], self.ignored)

    def unignore(self, chat_id, user):
        '''
        Unignores a user in a chat

        :param chat_id: Chat ID
        :param user: Username to ignored
        '''
        user = user.replace('@', '')
        self.ignored[chat_id].remove(user)

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
        # TODO: Make this not hacky with tries.
        try:
            self._last_id = self._bot.getUpdates()[-1].update_id
        except IndexError:
            self._last_id = None
        except telegram.error.TelegramError as e:
            logging.critical('Failed to start bot: {} (is your Telegram token correct?)'.format(e))
            sys.exit(1)

        logging.info('Started bot')

        try:
            while True:
                for update in self._bot.getUpdates(offset=self._last_id, timeout=10):
                    self._handle_msg(update)
        except KeyboardInterrupt:
            logging.info('Stopped bot')

lytebot = LyteBot()
