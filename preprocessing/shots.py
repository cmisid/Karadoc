import os

import click
import pandas as pd

from .base import Base


class ShotsProcessor(Base):

    """ Shots processor """

    def __init__(self, input_path='data/shots', output_path='features/shots'):
        super(ShotsProcessor, self).__init__(
            file_token='.jpg',
            input_path=input_path,
            output_path=output_path
        )

    def parse(self, doc):
        pass

    def run(self):
        for shot in self.shots_img:
            print(shot)
