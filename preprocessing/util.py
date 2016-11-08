import re


def remove_extra_html_tags(raw_html):
    """Remove extra HTML tags from a string already parsed by BeautifulSoup.
    Args:
        raw_html (str): A text containing HTML tags
    Returns:
        str: string without HTML tags
    """
    regex = re.compile('<.*?>')
    return re.sub(regex, '', raw_html)


def apply_func_dict_values(hash, f):
    """Method to apply a function to all hash values
    Args:
        hash (dict): The dictionnary where you want to apply a custom function
            on values.
        f (function): The function to apply to values.
    Output:
        dict: containing all input hash items after applying the function f
            on values.
    """
    return dict((k, f(v)) if isinstance(v, str) else (k, v) for k, v in hash.items())
