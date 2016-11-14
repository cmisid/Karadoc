import os
import json

import click
from collections import namedtuple
import cv2
import numpy as np
import pandas as pd
from scipy.ndimage.measurements import histogram
from scipy.misc import imread

from .base import Base
from .util import sample_image
from .util import sample_pixel
from .util import histogram_intersection
from .util import abs_path
from .util import write_json


class ShotsProcessorJPG(Base):

    """ Shots processor for jpeg files """

    def __init__(self, input_path='data/shots', output_path='features/shots'):
        super(ShotsProcessorJPG, self).__init__(
            file_token='.jpg',
            input_path=input_path,
            output_path=output_path
        )
        self.cascade_classifier_path = os.path.join('data', 'classifiers')

    def stream_files(self):
        """ Generator of image path """
        for folder, sub_folder, files in os.walk(self.input_path):
            for file in files:
                file_path = os.path.join(folder, file)
                if file_path.endswith(self.file_token):
                    yield file_path

    def compute_feature_detection(self, shot=None, cascade_classifier='haarcascade_frontalface_default.xml', scale_factor=1.3, min_neighbors=5):
        """ Detect faces in the image """

        # Read image
        img = cv2.imread(shot)

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # This loads the face cascade into memory so it’s ready for use. Remember,
        # the cascade is just an XML file that contains the trained data to detect faces.
        cascade = cv2.CascadeClassifier(os.path.join(
            self.cascade_classifier_path, cascade_classifier))

        # Detect faces in the image
        faces = cascade.detectMultiScale(gray, scale_factor, min_neighbors)

        Shot = namedtuple('slot', ['filename', 'shot', 'nb_faces'])

        face_text = '{0} face'.format(len(faces)) if len(
            faces) == 1 else '{0} faces'.format(len(faces))

        click.secho('{} --- {}'.format(face_text, shot), fg='yellow')

        return Shot(filename=os.path.basename(os.path.split(shot)[0]), shot=os.path.basename(shot), nb_faces=len(faces))

    def parse(self, doc):
        pass

    def run(self, batch_size=100):
        # Extract image histogram
        hist_data = {}
        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                print(abs_path(doc))
                img = cv2.imread(doc)
                hist_data[abs_path(doc)] = list(
                    map(
                        int,
                        cv2.calcHist([img], [0], None, [256], [0, 256]).ravel()
                    )
                )
        write_json(os.path.join(self.output_path, 'hist_data.json'), json.dumps(hist_data))

        # Extract the number of faces for each shot
        nb_faces = [self.compute_feature_detection(shot) for shot in self.stream_files()]
        faces_df = pd.DataFrame(nb_faces)
        faces_df.to_csv(os.path.join(self.output_path, 'faces_df.csv'))
