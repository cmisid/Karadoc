from sklearn.feature_extraction.text import HashingVectorizer

from .base import Base

class MetadataProcessor(Base):

    """Metadata processor"""

    def __init__(self, data_path):
        super(MetadataProcessor, self).__init__(
            data_path=data_path,
            file_token='*.xml'
        )

    def run(self, size=20):

        vectorizer = HashingVectorizer(non_negative=True)

        stream = self.stream_files()

        for minibatch in self.iter_minibatches(stream, size):
            print(len(minibatch))
