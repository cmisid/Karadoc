import os

from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from .base import Base
from .util import apply_func_dict_values
from .util import remove_extra_html_tags


class MetadataProcessor(Base):

    """Metadata processor"""

    def __init__(self, input_path='data/metadata', output_path='features/metadata'):
        super(MetadataProcessor, self).__init__(
            file_token='*.xml',
            input_path=input_path,
            output_path=output_path
        )

    def parse(self, doc):
        """Extract some components of a metadata video XML file
        Args:
            doc (str): file that has been opened
        Returns:
            dict: containing all metadatas features
        """
        soup = BeautifulSoup(doc, 'html.parser')
        # Feature extraction
        filename = soup.find('filename').get_text()
        title = soup.find('title').get_text()
        description = soup.find('description').get_text()
        duration = soup.find('duration').get_text()
        size = int(soup.find('size').get_text())
        explicit = soup.find('explicit').get_text()
        keywords = [
            tag.string
            for tag in soup.find('tags')
            if tag.string != '\n'
        ]
        licence = soup.find('licence').get_text() if soup.find('licence') else ''
        uploader = soup.find('uploader')
        uid = int(uploader.uid.get_text())
        login = uploader.login.get_text()

        features = dict(
            filename=filename,
            title=title,
            description=description,
            duration=duration,
            size=size,
            explicit=explicit,
            keywords=keywords,
            uploader_id=uid,
            uploader_login=login
        )
        return apply_func_dict_values(features, remove_extra_html_tags)

    def run(self, batch_size=100):

        vectorizer = CountVectorizer()
        term_frequency_dfs = []

        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            # 1. Extract term frequencies
            term_frequencies = vectorizer.fit_transform((
                doc['description'] for doc in minibatch
            ))
            term_frequency_dfs.append(pd.DataFrame(
                term_frequencies.todense(),
                index=(doc['title'] for doc in minibatch),
                columns=vectorizer.get_feature_names()
            ))

        features = pd.DataFrame()

        term_frequency_dfs = pd.concat(term_frequency_dfs).fillna(0)
        term_frequency_dfs.to_csv(os.path.join(self.output_path, 'term_frequencies.csv'))

    # TODO: Keywords occurence matrix
