import glob
import os

import click
from bs4 import BeautifulSoup
import pandas as pd

from .base import Base
from .util import filename_without_extension
from .util import to_seconds


class ShotsProcessorXML(Base):

    """ Shots processor for XML files """

    def __init__(self, input_path='data/shots', output_path='features/shots'):
        super(ShotsProcessorXML, self).__init__(
            file_token='*.xml',
            input_path=input_path,
            output_path=output_path
        )
        self.cascade_classifier_path = os.path.join('data', 'classifiers')

    def stream_files(self):
        """Stream files one by one."""
        for filename in glob.glob(os.path.join(self.input_path, self.file_token)):
            yield self.parse(open(filename, 'r').read())

    def parse(self, doc):
        """ Extract shots information
        Args:
            doc (str): file that has been opened
        Returns:
            dict: containing all shots features
        """
        soup = BeautifulSoup(doc, 'html.parser')

        frame = [
            frameid.get_text()
            for frameid in soup.find_all('keyframeid')
        ]

        segments = [
            (to_seconds(segment['start']), to_seconds(segment['end']))
            for segment in soup.find_all('segment')
        ]

        return {
            'filenames': frame,
            'segments': segments
        }

    def run(self, batch_size=100):

        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                print(doc)
