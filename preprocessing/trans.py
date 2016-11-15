import glob
import os

import click
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from .base import Base
from .util import filename_without_extension


class TransProcessor(Base):

    """ Trans processor """

    def __init__(self, input_path='data/trans', output_path='features/trans'):
        super(TransProcessor, self).__init__(
            file_token='*.xml',
            input_path=input_path,
            output_path=output_path
        )
        self.word_confidence = 0.8

    def stream_files(self):
        """Stream files one by one."""
        for filename in glob.glob(os.path.join(self.input_path, self.file_token)):
            yield self.parse(open(filename, 'r').read())

    def parse(self, doc):
        """ Extract transcriptions
        Args:
            doc (str): file that has been opened
        Returns:
            dict: containing all transcriptions features
        """

        soup = BeautifulSoup(doc, 'html.parser')
        # Transcription extraction
        words = [
            word.get_text().replace(' ', '')
            for word in soup.find_all('word')
            if (float(word['conf']) > self.word_confidence)
        ]

        return {
            'filename': filename_without_extension(soup.find('audiodoc')['name']),
            'trans': ' '.join(words)
        }

    def run(self, batch_size=100):
        vectorizer = CountVectorizer()

        trans_tf_dfs = []

        click.secho('Iterating through files to extract transcription...', fg='blue', bold=True)
        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            trans_tf = vectorizer.fit_transform((
                doc['trans'] for doc in minibatch
            ))
            trans_tf_dfs.append(pd.DataFrame(
                trans_tf.todense(),
                index=(doc['filename'] for doc in minibatch),
                columns=vectorizer.get_feature_names()
            ))

        click.secho('Saving trans frequencies', fg='cyan')
        trans_tf_dfs = pd.concat(trans_tf_dfs, axis=0, ignore_index=False)
        trans_tf_dfs.to_csv(os.path.join(self.output_path, 'tf_trans.csv'))
