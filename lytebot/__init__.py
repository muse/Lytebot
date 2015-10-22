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
    with open('{}/config.json'.format(config_dir)) as f:
        config = json.load(f)
except FileNotFoundError:
    logging.critical('Configuration file was not found. Does \'{}/config.json\' exist?'.format(config_dir))
    sys.exit(1)
