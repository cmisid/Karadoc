import hashlib
import hmac
import os
import re
import string

import nltk
from nltk.stem import WordNetLemmatizer


def tokenize(text):
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def remove_extra_html_tags(raw_html):
    """ Remove extra HTML tags from a string already parsed by BeautifulSoup.
    Args:
        raw_html (str): A text containing HTML tags
    Returns:
        str: string without HTML tags
    """
    regex = re.compile('<.*?>')
    return re.sub(regex, '', raw_html)


def apply_func_dict_values(hash, f):
    """ Method to apply a function to all hash values
    Args:
        hash (dict): The dictionary where you want to apply a custom function
            on values.
        f (function): The function to apply to values.
    Output:
        dict: containing all input hash items after applying the function f
            on values.
    """
    return dict((k, f(v)) if isinstance(v, str) else (k, v) for k, v in hash.items())


def make_hash(string, hash_key='karadoc'):
    """ Generate a unique id (hash) with a hash key
    Args:
        string (str): a string
    Output:
        str: a string converted to hash using sha256 conversion algorithm
    """
    digest = hmac.new(key=bytes(hash_key, 'utf-8'),
                      msg=bytes(string, 'utf-8'),
                      digestmod=hashlib.sha256).hexdigest()
    return str(digest)


def filename_without_extension(filename):
    """ Extract the filename and remove the file extension (eg .jpg) """
    return os.path.splitext(filename)[0]
