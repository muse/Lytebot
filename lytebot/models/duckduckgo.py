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
    first = soup(attrs={'class': 'results_links results_links_deep web-result'})[0]
    url = first.find('a', class_='large')

    return url['href'] if url else 'I got nuthing!'

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

    if resp.geturl():
        base_url = urllib.parse.urlparse(resp.geturl())
        return search('site:{} {}'.format(base_url.netloc, query))

    return 'What happend!?'
