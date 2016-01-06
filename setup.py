#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Lytebot',
    version='1.0.0',
    author='soud',
    author_email='soud@protonmail.com',
    description='Lytebot is a telegram bot existing of some convenient and fun functionalities.',
    license='MIT',
    keywords='telegram bot',
    url='https://github.com/muse/Lytebot',
    packages=['lytebot', 'lytebot.models', 'lytebot.commands'],
    long_description=long_description,
    install_requires=[
        'imgurpython==1.1.6',
        'PyYAML==3.11',
        'python-telegram-bot==3.2.0',
        'beautifulsoup4==4.4.1',
    ],
    classifiers=[
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
    scripts=['bin/lytebot']
)
