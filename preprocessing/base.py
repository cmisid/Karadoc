from glob import glob
import itertools
import os


class Base():

    def __init__(self, data_path, file_token):
        self.data_path = data_path
        self.file_token = file_token

    def parse(self, doc):
        raise NotImplementedError

    def stream_files(self):
        """Stream files one by one."""
        for filename in glob(os.path.join(self.data_path, self.file_token)):
            for doc in self.parse(open(filename, 'r')):
                yield doc

    def get_minibatch(self, stream, size):
        """A minibatch is a stream slice."""
        return [doc for doc in itertools.islice(stream, size)]

    def iter_minibatches(self, stream, minibatch_size):
        """Generator of minibatches."""
        minibatch = self.get_minibatch(stream, minibatch_size)
        while len(minibatch):
            yield minibatch
            minibatch = self.get_minibatch(stream, minibatch_size)

    def run(self):
        raise NotImplementedError
