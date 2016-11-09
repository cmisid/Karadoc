import os

from bs4 import BeautifulSoup
import click
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from .base import Base
from .util import apply_func_dict_values
from .util import remove_extra_html_tags
from .util import filename_without_extension


class MetadataProcessor(Base):

    """ Metadata processor """

    def __init__(self, input_path='data/metadata', output_path='features/metadata'):
        super(MetadataProcessor, self).__init__(
            file_token='*.xml',
            input_path=input_path,
            output_path=output_path
        )

    def parse(self, doc):
        """ Extract some components of a metadata video XML file
        Args:
            doc (str): file that has been opened
        Returns:
            dict: containing all metadatas features
        """
        soup = BeautifulSoup(doc, 'html.parser')

        # Feature extraction
        keywords = [
            tag.string
            for tag in soup.find('tags')
            if tag.string != '\n'
        ]

        document = dict(
            filename=filename_without_extension(soup.find('filename').get_text()),
            title=soup.find('title').get_text(),
            description=soup.find('description').get_text(),
            duration=soup.find('duration').get_text(),
            size=int(soup.find('size').get_text()),
            explicit=soup.find('explicit').get_text(),
            keywords=keywords,
            licence=soup.find('licence').get_text() if soup.find('licence') else '',
            uploader_id=int(soup.find('uploader').uid.get_text()),
            uploader_login=soup.find('uploader').login.get_text()
        )

        return apply_func_dict_values(document, remove_extra_html_tags)

    def run(self, batch_size=100):

        vectorizer = CountVectorizer()
        term_frequency_dfs = []
        keyword_frequency_dfs = []
        title_frequency_dfs = []
        features_dfs = []

        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            # 1. Extract term frequencies
            term_frequencies = vectorizer.fit_transform((
                doc['description'] for doc in minibatch
            ))
            term_frequency_dfs.append(pd.DataFrame(
                term_frequencies.todense(),
                index=(doc['filename'] for doc in minibatch),
                columns=vectorizer.get_feature_names()
            ))
            # 2. Extract features from documents
            df_batch_features = pd.DataFrame(minibatch)
            df_batch_features.set_index('filename', inplace=True)
            columns_to_delete = ['description', 'keywords']
            df_batch_features.drop(columns_to_delete, axis=1, inplace=True)
            features_dfs.append(df_batch_features)

            # 3. Extract keywords frequencies
            keyword_frequencies = vectorizer.fit_transform((
                " ".join(doc['keywords']) for doc in minibatch
            ))
            keyword_frequency_dfs.append(pd.DataFrame(
                keyword_frequencies.todense(),
                index=(doc['filename'] for doc in minibatch),
                columns=vectorizer.get_feature_names()
            ))

            # 4. Extract title frequencies
            title_frequencies = vectorizer.fit_transform((
                doc['title'] for doc in minibatch
            ))
            title_frequency_dfs.append(pd.DataFrame(
                title_frequencies.todense(),
                index=(doc['filename'] for doc in minibatch),
                columns=vectorizer.get_feature_names()
            ))

        features_dfs = pd.concat(features_dfs, axis=0, ignore_index=False)
        features_dfs.to_csv(os.path.join(self.output_path, 'features.csv'))
        term_frequency_dfs = pd.concat(term_frequency_dfs).fillna(0)
        term_frequency_dfs.to_csv(os.path.join(self.output_path, 'tf_description.csv'))
        keyword_frequency_dfs = pd.concat(keyword_frequency_dfs).fillna(0)
        keyword_frequency_dfs.to_csv(os.path.join(self.output_path, 'tf_keywords.csv'))
        title_frequency_dfs = pd.concat(title_frequency_dfs).fillna(0)
        title_frequency_dfs.to_csv(os.path.join(self.output_path, 'tf_titles.csv'))

    # TODO: Keywords occurence matrix
    # liste de phrases concaténées + index filename
