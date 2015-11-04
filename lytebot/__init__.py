import os
import sys
import json
import logging
import lytebot

config_dir = os.path.expanduser('~/.config/lytebot')

# set up logging
log_format = '%(asctime)s [%(levelname)-5.5s] %(message)s'
logging.basicConfig(filename=os.path.join(config_dir, 'lytebot.log'),
                    format=log_format, level=logging.INFO)

# stdout logger
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(log_format))

logging.getLogger('').addHandler(console)

# config file loading
if not os.path.isdir(config_dir):
    try:
        logging.info('Creating config directory')
        os.mkdir(config_dir)
    except FileExistsError:
        pass

try:
    with open(os.path.join(config_dir, 'config.json'), 'r') as f:
        config = json.load(f)
        if 'owners' in config['telegram'] and config['telegram']['owners']:
            logging.info('Found owners: {}'.format(', '.join(config['telegram']['owners'])))
except FileNotFoundError:
    logging.critical('Configuration file was not found. Does \'{}\' exist?'.format(os.path.join(config_dir, 'config.json')))
    sys.exit(1)
