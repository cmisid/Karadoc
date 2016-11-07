import os
import re

from bs4 import BeautifulSoup


def remove_extra_html_tags(raw_html):
    ''' Remove extra HTML tags from a string already parsed by BeautifulSoup. 
    Args: 
        - raw_html (str): A text containing HTML tags
    Output:
        - str: string without HTML tags
    '''
    regex = re.compile('<.*?>')
    return re.sub(regex, '', raw_html)


def apply_func_dict_values(hash, f):
    ''' Method to apply a function to all hash values 
    Args:
        - hash (dict): The dictionnary where you want to apply a custom function on values
        - f (function): The function to apply to values
    Output:
        - (dict): containing all input hash items after applying the function f on values
    '''
    return dict((k, f(v)) for k, v in hash.items())


def extract_metadata_features(doc):
    ''' Extract some components of a metadata video XML file 
    Args:
        - document (str): file that has been opened
    Output:
        - (dict): containing all metadatas features
    '''
    soup = BeautifulSoup(doc, 'html.parser')
    # Feature extraction
    title = soup.find('title').get_text()
    description = soup.find('description').get_text()
    duration = soup.find('duration').get_text()
    size = soup.find('size').get_text()

    features = dict(
        title=title,
        description=description,
        duration=duration,
        size=size
    )
    return apply_func_dict_values(features, remove_extra_html_tags)


filename = 'data/metadata/Aabbey1-InvitationToSummer2009RabbinicalStudySeminarAtHartmanIn262.xml'
doc = open(filename).read()
features = extract_metadata_features(doc)
