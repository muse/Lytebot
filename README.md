# Lytebot
Lytebot is a Telegram bot existing of some convenient and fun features like searching
DuckDuckGo, random image from a subreddit and searching specific sites through
DuckDuckGo's [!bangs](https://duckduckgo.com/bang)

# Installation
## Dependencies
- imgurpython
- python-telegram-bot
- Python 3.x

## Building
```bash
$ git clone https://github.com/Imakethings/Lytebot
$ cd Lytebot
$ pip install -r requirements.txt
$ sudo ./setup.py install
```

This will put the executable `lytebot` in your path. To use the bot, you need
to put the example configuration file in `~/.lytebot/config.json` with your Imgur
id and secret and Telegram token.
