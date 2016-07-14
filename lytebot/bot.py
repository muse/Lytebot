import os
import re
import sys
import time
import logging
import telegram
import yaml
import threading

from urllib.error import URLError
from lytebot import config, config_dir
from lytebot.errors import CommandError

class LyteBot:
    paths = {
        'ignored': os.path.join(config_dir, 'ignored.yml'),
        'disabled': os.path.join(config_dir, 'disabled.yml'),
        'blacklisted': os.path.join(config_dir, 'blacklisted.yml'),
    }

    def __init__(self):
        '''Initialize bot'''
        self.prefix = '/'
        self.ignored = {}
        self.commands = {}
        self.disabled = []
        self.previous = {}
        self.blacklisted = []
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
        '''
        Handles all messages sent in all chats (that the bot can see)

        :param update: Object with chat info
        '''
        # Ignore stickers, pictures and other non-text messages
        if not update['message'] or not update.message['text']:
            return

        # Is the user who sent the message ignored?
        if update.message.chat_id in self.ignored and \
           update.message.from_user.username in self.ignored[update.message.chat_id]:
            return

        message = update.message.text[1::]
        prefix = update.message.text[0]
        command = self.get_command(message)
        user = update.message.from_user.username or update.message.from_user.first_name

        if command and prefix == self.prefix and not self._is_disabled(command):
            # Check if the user is an owner if he calls an admin command
            if command['admin'] and update.message.from_user.username not in config['telegram']['owners']:
                text = '@{} You can\'t do that!'.format(user)
            else:
                text = command['func'](update.message, user)

            t = threading.Thread(target=self._bot.sendMessage, kwargs={
                'chat_id': update.message.chat_id,
                'text': text
            })
            t.start()

            self._last_id = update.update_id + 1

            if not message.startswith('!!'):
                self._set_previous(command['func'], update.message)

    def is_command(self, command):
        '''
        Check if a command exists

        :param command: Name to check
        :rtype: bool
        '''
        return command['func'].__name__ in self.commands

    def blacklist(self, sub):
        '''
        Blacklist a sub from the /r command

        :param sub: Subreddit to blacklist
        '''
        if sub not in self.blacklisted:
            self.blacklisted.append(sub.lower())
            self.save_data(self.paths['blacklisted'], self.blacklisted)

    def whitelist(self, sub):
        '''
        Whitelist a sub from the /r command

        :param sub: Subreddit to whitelist
        '''
        try:
            self.blacklisted.remove(sub.lower())
        except ValueError:
            return

        self.save_data(self.paths['blacklisted'], self.blacklisted)

    def disable(self, command):
        '''
        Disables a command in _all_ chats

        :param command: Command to disables
        :raises: CommandError
        '''
        if self._is_disabled(command):
            raise CommandError('Command {} already disabled'.format(command['func'].__name__))

        if not self.is_command(command):
            raise CommandError('Command {} doesn\'t exist'.format(command['func'].__name__))

        self.disabled.append(command['func'].__name__)
        self.save_data(self.paths['disabled'], self.disabled)

    def _is_disabled(self, command):
        '''
        Check if command is disabled

        :param command: Command to check
        :rtype: bool
        '''
        return command['func'].__name__ in self.disabled

    def enable(self, command):
        '''
        Enables a command in _all_ chats

        :param command: Command to enable
        :raises: CommandError
        '''
        if self._is_enabled(command):
            raise CommandError('Command {} isn\'t disabled'.format(command['func'].__name__))

        if not self.is_command(command):
            raise CommandError('Command {} doesn\'t exist'.format(command['func'].__name__))

        self.disabled.remove(command['func'].__name__)
        self.save_data(self.paths['disabled'], self.disabled)

    def _is_enabled(self, command):
        '''
        Check if command is enabled

        :param command: Command to check
        :rtype: bool
        '''
        return not self._is_disabled(command)

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
        :param user: Username to ignore
        '''
        if chat_id not in self.ignored:
            self.ignored[chat_id] = []

        if user not in self.ignored[chat_id]:
            # allow /ignore @username for convenience
            user = user.replace('@', '')
            self.ignored[chat_id].append(user)

        self.save_data(self.paths['ignored'], self.ignored)

    def unignore(self, chat_id, user):
        '''
        Unignores a user in a chat

        :param chat_id: Chat ID
        :param user: Username to unignore
        '''
        user = user.replace('@', '')
        self.ignored[chat_id].remove(user)

        self.save_data(self.paths['ignored'], self.ignored)

    def command(self, handle, admin=False):
        '''
        Create a new command entry, saved in self.commands

        :param handle: The name for the command
        :param admin: Is the command meant for owners only?
        :rtype: function
        '''
        def arguments(function):
            self.commands[handle] = {'admin': admin, 'func': function}
            logging.info('Found command -> {}'.format(function.__name__))
            return self.commands
        return arguments

    def get_command(self, message):
        '''
        Gets command from message sent, if it contains a command

        :param message: Message that could contain a command
        :rtype: function or None
        '''
        try:
            bot_name = self._bot.getMe()['username']
        except Exception as e:
            logging.warning(e)
            return None

        for command in self.commands:
            pattern = r'^({0}@{1}$|{0}$|{0}(@{1}|)\ \w*)'.format(command, bot_name)

            if re.match(pattern, message):
                return self.commands[command]

        return None

    def run(self):
        '''Start listening for commands'''
        logging.info('Started bot')

        try:
            self._last_id = self._bot.getUpdates()[0].update_id
        except (IndexError, KeyError):
            self._last_id = None

        while True:
            try:
                updates = self._bot.getUpdates(offset=self._last_id, timeout=10)
            except telegram.error.TelegramError as e:
                if e.message in ("Bad Gateway", "Timed out"):
                    time.sleep(1)
                    continue
                elif e.message == "Unauthorized":
                    update_id += 1
                else:
                    logging.critical('Failed to start bot: {} (is your Telegram token correct?)'.format(e))
                    sys.exit(1)
            except URLError as e:
                time.sleep(1)
                continue

            for update in updates:
                self._handle_msg(update)

lytebot = LyteBot()
