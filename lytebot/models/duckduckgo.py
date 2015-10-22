import urllib
import logging
from bs4 import BeautifulSoup

def search(query):
    url = 'https://duckduckgo.com/html/?q={}'.format(urllib.parse.quote_plus(query))

    try:
        resp = urllib.request.urlopen(url)
    except Exception as e:
        logging.info('DuckDuckGo: {}'.format(e))
        return 'Something went wrong!!'

    soup = BeautifulSoup(resp, 'html.parser')
    container = soup.find('div', class_='links_main')
    url = container.find('a', class_='large')

    return url['href'] if url['href'] else 'I got nuthing!'

def bang_search(bang, query):
    url = 'https://duckduckgo.com/html/?q={}+{}'.format(bang, urllib.parse.quote_plus(query))

    try:
        resp = urllib.request.urlopen(url)
    except Exception as e:
        logging.info('DuckDuckGo: {}'.format(e))
        return 'Something went wrong!!'

    # if it didn't redirect, the bang is invalid
    if resp.geturl().startswith('https://duckduckgo.com'):
        return 'Invalid bang: {}'.format(bang)
    return resp.geturl() if resp.geturl() else 'What happend?'
