import os
import sys
import json
import logging

config_dir = os.path.expanduser('~/.lytebot')

if not os.path.isdir(config_dir):
    try:
        logging.info('Creating config directory')
        os.mkdir(config_dir)
    except FileExistsError:
        pass

try:
    with open(os.path.join(config_dir, 'config.json'), 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logging.critical('Configuration file was not found. Does \'{}\' exist?'.format(os.path.join(config_dir, 'config.json')))
    sys.exit(1)
