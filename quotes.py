import random

import click
import requests

from bs4 import BeautifulSoup

URL = 'https://fr.wikiquote.org/wiki/Kaamelott/Karadoc'


def parse_wikiquote():
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
    quotes = parse_wikiquote()
    quote, ref = random.choice(quotes)
    click.secho(quote, blink=True, fg='cyan')
    click.secho('{}--- {}'.format('\t' * 3, ref), blink=True, fg='white')

random_quote()
