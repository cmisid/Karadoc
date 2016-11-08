import random

import click
import requests

from bs4 import BeautifulSoup

URL = 'https://fr.wikiquote.org/wiki/Kaamelott/Karadoc'


def parse_wikiquote():
	""" Crawl Karadoc wikiquote page to retrieve his most famous quotes. """

    response = requests.get(URL)
    assert response.status_code
    
    soup = BeautifulSoup(response.text, 'html.parser')

    clean = lambda x: x.replace('\xa0', '')

    citations = [
        clean(citation.get_text())
        for citation in soup.find_all('span', attrs={'class': 'citation'})
    ]

    references = [
        clean(ref.get_text())
        for ref in soup.find_all('div', attrs={'class': 'ref'})
    ]

    return list(zip(citations, references))


def random_quote():
	""" Compute a random choice between a list of famous quotes 
	and print them to stdout.
	"""

    quotes = parse_wikiquote()
    quote, ref = random.choice(quotes)
    click.secho(quote, blink=True, fg='cyan')
    click.secho('{}--- {}'.format('\t' * 3, ref), blink=True, fg='white')


@click.command()
@click.option('--quote/--no-quote', help='Try me ;)', default=False)
def karadoc(quote):
    if quote:
        random_quote()

if __name__ == '__main__':
    karadoc()
