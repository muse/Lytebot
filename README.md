# Lytebot
Lytebot is a Telegram bot existing of some convenient and fun features like searching
DuckDuckGo, random image from a subreddit and searching specific sites through
DuckDuckGo's [!bangs](https://duckduckgo.com/bang).

# Usage
Visit https://telegram.me/Lytebot, or send a message to @Lytebot.

## Commands
- /r [sub]: Random image by subreddit
- /ddg [query]: Search DuckDuckGo
- /flip: (╯°□°)╯︵ ┻━┻
- /back: ┬─┬ ノ( ゜-゜ノ)
- /disabled: Show disabled commands
- /![bang] [query]: Search DuckDuckGo by bang

## Owner commands
- /disable [command]: Disable a command
- /enable [command]: Enable a command
- /ignore [user]: Ignore a user (don't execute commands sent by user)
- /unignore [user]: Unignore a user
- /blacklist [sub]: Blacklist subreddit from /r command
- /whitelist [sub]: Whitelist subreddit from /r command

# Installation
## Dependencies
- Python 3.x
- beautifulsoup4
- imgurpython
- PyYAML
- python-telegram-bot

## Building
```bash
$ git clone https://github.com/muse/Lytebot
$ cd Lytebot
$ ./setup.py install
```

This will put the executable `lytebot` in your path.

## Configuring
To use the bot, you need to put the example configuration file in
`~/.config/lytebot/config.yml` with your Telegram token.

If you wish to use owner commands, you need to set the owner(s) usernames in
`~/.config/lytebot/config.yml`. The same goes for the Imgur commands, you'll
need to put your Imgur ID and secret in the config file.

If something breaks or goes wrong, you can see the log file found in
`~/.config/lytebot`.
