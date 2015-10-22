#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'lytebot',
    version = '0.0.1',
    author = 'soud',
    author_email = 'soud@protonmail.com',
    description = 'A practical telegram bot.',
    license = 'MIT',
    keywords = 'telegram bot',
    url = 'https://github.com/Imakethings/Lytebot',
    packages = ['lytebot', 'lytebot.models', 'lytebot.commands'],
    long_description = open('README.md').read(),
    classifiers = [
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP'
    ],
    scripts = ['bin/lytebot']
)
