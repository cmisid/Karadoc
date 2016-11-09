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
    click.secho('{}--- {}'.format('\t' * 3, ref), fg='white')


def render_karadoc():
    logo = ''' _   __  ___  ______   ___  ______  _____  _____ 
| | / / / _ \ | ___ \ / _ \ |  _  \|  _  |/  __ \ 
| |/ / / /_\ \| |_/ // /_\ \| | | || | | || /  \/ 
|    \ |  _  ||    / |  _  || | | || | | || |    
| |\  \| | | || |\ \ | | | || |/ / \ \_/ /| \__/\ 
\_| \_/\_| |_/\_| \_|\_| |_/|___/   \___/  \____/ 
    '''
    click.secho(str(logo), fg='yellow', bold=True)
    click.secho('{}--- {}'.format('\t' * 1, 'TAGGING VIDEOS (MEDIAEVAL CHALLENGE)'), fg='white')


@click.command()
@click.option('--quote/--no-quote', help='Try me ;)', default=False)
@click.option('--verbose/--no-verbose', '-v', help='Verbose output', default=False)
def karadoc(quote, verbose):
    if verbose:
        render_karadoc()
    if quote:
        random_quote()

if __name__ == '__main__':
    karadoc()
