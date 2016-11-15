import glob
import os

from .base import Base


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
            yield self.parse(open(filename, 'r').read())

    def parse(self, doc):
        """ Extract shots information
        Args:
            doc (str): file that has been opened
        Returns:
            dict: containing all shots features
        """
        return doc

    def run(self, batch_size=100):

        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                print(doc)
