from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

from .base import Base
from .util import apply_func_dict_values
from .util import remove_extra_html_tags

class MetadataProcessor(Base):

    """Metadata processor"""

    def __init__(self, data_path):
        super(MetadataProcessor, self).__init__(
            data_path=data_path,
            file_token='*.xml'
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

    def run(self, size=20):

        vectorizer = TfidfVectorizer()

        stream = self.stream_files()

        for minibatch in self.iter_minibatches(stream, size):
            X_train = vectorizer.fit_transform((
                doc['description'] for doc in minibatch
            ))
            print(type(X_train))
