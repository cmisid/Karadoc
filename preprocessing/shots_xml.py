import glob
import itertools
import os

import click
from collections import namedtuple
from bs4 import BeautifulSoup
import pandas as pd

from .base import Base
from .util import to_seconds
from .util import shot_name


class ShotsProcessorXML(Base):

    """ Shots processor for XML files """

    def __init__(self, input_path='data/shots', output_path='features/shots'):
        super(ShotsProcessorXML, self).__init__(
            file_token='*.xml',
            input_path=input_path,
            output_path=output_path
        )

    def stream_files(self):
        """Stream files one by one."""
        for filename in glob.glob(os.path.join(self.input_path, self.file_token)):
            yield open(filename, 'r').read()

    def extract_shots(self, doc):
        soup = BeautifulSoup(doc, 'html.parser')
        filename = soup.find('creationid').get_text()

        Shot = namedtuple('shot', ['filename', 'shot', 'duration'])

        shots = [shot_name(shot.get_text()) for shot in soup.find_all('keyframeid')]
        shot_duration = [
            to_seconds(segment['end']) - to_seconds(segment['start'])
            for segment in soup.find_all('segment')
        ][:-1]
        # We need to change the value of the last 'end' segment because it
        # does not correspond to the total video duration
        # Video duration is available into the 'features/metadata/features.csv'
        try:
            metadatas = pd.read_csv('features/metadata/features.csv')
        except FileNotFoundError as err:
            click.secho(
                'You need to launch the MetadataProcessor before to have the `features.csv` dataframe. \n {}'.format(err), fg='red')

        duration = int(metadatas[metadatas.filename == filename].duration.item())

        last_segment_start = [
            to_seconds(segment['start'])
            for segment in soup.find_all('segment')
        ][-1]

        shot_duration.append(duration - last_segment_start)

        assert len(shots) == len(shot_duration)

        return [
            Shot(filename=filename, shot=shots[i], duration=shot_duration[i])
            for i, _ in enumerate(shots)
        ]

    def parse(self, doc):
        pass

    def run(self, batch_size=100):
        shots_duration_df = []
        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                shots_duration_df.append(self.extract_shots(doc))
        shots_duration_df = list(itertools.chain(*shots_duration_df))
        shots_duration_df = pd.DataFrame(shots_duration_df)
        shots_duration_df.to_csv(os.path.join(self.output_path, 'shots_duration_df.csv'))
