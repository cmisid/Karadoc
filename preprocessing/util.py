import hashlib
import hmac
import json
import os
import re
import string

import nltk
from nltk.stem import WordNetLemmatizer


def tokenize(text):
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmes = [lemmatizer.lemmatize(token) for token in tokens]
    return [l for l in lemmes if len(l) > 2]


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
    return re.sub(r'\.\w*', '', filename)


def histogram_intersection(h1, h2):
    return sum(((min(v1, v2) for v1, v2 in zip(h1, h2))))


def sample_pixel(pixel):
    to_bits = lambda x: '{0:08b}'.format(x)
    r, g, b = to_bits(pixel[0]), to_bits(pixel[1]), to_bits(pixel[2])
    r_intensity = int(r[0]) * 2 ** 5 + int(r[1]) * 2 ** 4
    g_intensity = int(g[0]) * 2 ** 3 + int(g[1]) * 2 ** 2
    b_intensity = int(b[0]) * 2 ** 1 + int(b[1]) * 2 ** 0
    intensity = r_intensity + g_intensity + b_intensity
    return [intensity, intensity, intensity]


def sample_image(image):
    return [
        [
            sample_pixel(pixel)
            for pixel in row
        ]
        for row in image
    ]


def read_json(file):
    with open(file, 'r') as json_data:
        return json.load(json_data)


def write_json(file, data):
    with open(file, 'w') as json_data:
        json_data.write(data)


def video_name(shot_path):
    return os.path.basename(os.path.split(shot_path)[0])


def shot_name(shot_path):
    return os.path.basename(shot_path)


def abs_path(file):
    return os.path.join(
        os.path.basename(os.path.split(file)[0]),
        os.path.basename(file)
    )


def to_seconds(keyframe_time):
    _, minutes, seconds, _ = keyframe_time.split(':')
    return int(minutes) * 60 + int(seconds) if int(minutes) != 0 else int(seconds)
