import pytest
import sure


import os
import sys

# Update sys.path to access preprocessing folder
sys.path.insert(0, os.getcwd())
os.chdir(os.getcwd())

import preprocessing.util


@pytest.fixture()
def html_tags():
    return [
        '<a>A formatted text into HTML tags</a>',
        '<body><p> This is first Paragraphs </p><p> This is Second Paragraphs </p></body>',
        '<h1> Heading Tag </h1>',
        '<i> Italic text </i>'
    ]


@pytest.fixture()
def dict_with_html_tags():
    return {
        'explicit': 'false',
        'keywords': ['short', 'films', 'florida', 'miami'],
        'title': 'Short Films - Dawn Dubriels - The Last Dutchess',
        'size': '21489618',
        'duration': '302',
        'description': '<p>Underlab Studios Presents:</p><p>Dawn Dubriels - "The Last Dutchess"<br />Starring: J.Vinazza, Amber Dubriel, & Film Carlucci<br /><br />Based on Robert Browning Poem of the Same Name, A Dutchess goes to a famous artist to get her portrait done. But her boyfriend has an alternate plan for the sly painter.</p>For More Information visit - <a href="http://www.myspace.com/dawndubriel">Dawn Dubriels Film Page</a>'
    }


def test_extra_html_removed(html_tags):
    preprocessing.util.should.have.property(
        'remove_extra_html_tags').being.callable
    for html_tag in html_tags:
        html_tag.should.be.a(str)
        formatted = preprocessing.util.remove_extra_html_tags(html_tag)
        formatted.should.be.a(str)
        formatted.should_not.be.equal(html_tag)


def test_apply_func_dict_values_success(dict_with_html_tags):
    preprocessing.util.should.have.property(
        'apply_func_dict_values').being.callable
    function = preprocessing.util.remove_extra_html_tags
    cleaned_dict = preprocessing.util.apply_func_dict_values(
        dict_with_html_tags, function)
    cleaned_dict.should.be.a(dict)
    for k, v in cleaned_dict.items():
        if isinstance(v, str):
            v.should.be.equal(preprocessing.util.remove_extra_html_tags(v))
