from .base import Base


class TransProcessor(Base):

    """ Trans processor """

    def __init__(self):
        def __init__(self, input_path='data/trans', output_path='features/trans'):
            super(TransProcessor, self).__init__(
                file_token='*.xml',
                input_path=input_path,
                output_path=output_path
            )

    def parse(self, doc):
        pass

    def run(self, **kwargs):
        pass
