import os
import json

from collections import namedtuple, defaultdict
import click
import cv2
import pandas as pd

from .base import Base
from .util import abs_path
from .util import read_json
from .util import shot_name
from .util import write_json
from .util import video_name


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

        # TODO: do everything in one single loop

        # 1. Extract image histogram
        hist_data = {}
        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                img = cv2.imread(doc)
                hist_data[abs_path(doc)] = list(
                    map(
                        int,
                        cv2.calcHist([img], [0], None, [256], [0, 256]).ravel()
                    )
                )
        write_json(os.path.join(self.output_path, 'hist_data.json'), json.dumps(hist_data))

        # 2. Extract the number of faces for each shot
        nb_faces = [self.compute_feature_detection(shot) for shot in self.stream_files()]
        faces_df = pd.DataFrame(nb_faces)
        faces_df.to_csv(os.path.join(self.output_path, 'faces_df.csv'))

        # 3. Extract the number of shots per video
        nb_shots_per_video = defaultdict(list)
        nb_shots_df = []
        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                nb_shots_per_video[video_name(doc)].append(shot_name(doc))

        Entry = namedtuple('entry', ['video', 'nb_shots'])

        for key in nb_shots_per_video.keys():
            nb_shots_df.append(Entry(video=key, nb_shots=len(nb_shots_per_video[key])))

        nb_shots_df = pd.DataFrame(nb_shots_df)
        nb_shots_df.sort_values(by='nb_shots', ascending=False, inplace=True)
        nb_shots_df.to_csv(os.path.join(self.output_path, 'nb_shots_df.csv'), index=False)

        # 4. Detect if an image is of one single color (black, blue, etc.)
        histograms = read_json(os.path.join(self.output_path, 'hist_data.json'))

        single_colors = []
        for img, histogram in histograms.items():
            ratios = [i / sum(histogram) for i in histogram] # Normalize the histogram
            is_single_color = False
            for ratio in ratios:
                if ratio >= 0.99:
                    is_single_color = True
                    break # No need to check other bars
            row = [str(img).split('/')[0], str(img).split('/')[1], is_single_color]
            single_colors.append(row)
            print(str(img))

        single_colors_df = pd.DataFrame(single_colors, columns=('filename', 'shot', 'single_color'))
        single_colors_df.to_csv(os.path.join(self.output_path, 'single_colors.csv'), index=False)
