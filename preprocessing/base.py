import itertools


class Base():

    def __init__(self, file_token, input_path, output_path):
        self.file_token = file_token
        self.input_path = input_path
        self.output_path = output_path

    def parse(self, doc):
        raise NotImplementedError

    def run(self, **kwargs):
        raise NotImplementedError

    def stream_files(self):
        raise NotImplementedError

    def get_minibatch(self, stream, size):
        """A minibatch is a stream slice."""
        return [doc for doc in itertools.islice(stream, size)]

    def iter_minibatches(self, stream, minibatch_size):
        """Generator of minibatches."""
        minibatch = self.get_minibatch(stream, minibatch_size)
        while len(minibatch):
            yield minibatch
            minibatch = self.get_minibatch(stream, minibatch_size)
