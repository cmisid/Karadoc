import glob
import os
import subprocess
from collections import defaultdict

import click
import librosa
import numpy as np
import pandas as pd
import sklearn

from scipy.io import wavfile

from .base import Base
from .util import filename_without_extension
from .util import audio_file_path


class SignalProcessor(Base):

    """ Signal processor for .ogv files """

    def __init__(self, input_path='data/videos', output_path='features/audio'):
        super(SignalProcessor, self).__init__(
            file_token='.flv.ogv',
            input_path=input_path,
            output_path=output_path
        )

    def stream_files(self):
        """ Generator of image path """
        for folder, sub_folder, files in os.walk(self.input_path):
            for file in files:
                file_path = os.path.join(folder, file)
                if file_path.endswith(self.file_token):
                    yield self.parse(file_path)

    @staticmethod
    def convert_video_to_audio(doc):
        audio_file = audio_file_path(doc)
        cmd = 'ffmpeg -loglevel panic -i {input_file} -acodec pcm_s16le -ac 1 -ar 16000 {output_file}'.format(
            input_file=doc,
            output_file=audio_file
        )
        try:
            subprocess.call(cmd, shell=True)
            click.secho('`{}` created.'.format(audio_file), fg='cyan')
        except Exception as err:
            raise err

    @staticmethod
    def remove_audio_file(doc):
        audio_file = audio_file_path(doc)
        try:
            os.remove(audio_file)
            click.secho('`{}` deleted.'.format(audio_file), fg='cyan')
        except Exception as err:
            raise err

    def parse(self, doc):
        return doc

    def run(self, batch_size=5):
        click.secho('Iterating through videos to extract audio signal...', fg='blue', bold=True)

        features = defaultdict(list)
        for minibatch in self.iter_minibatches(self.stream_files(), batch_size):
            for doc in minibatch:
                # Use ffmpeg CLI to convert .ogv files to .wav
                self.convert_video_to_audio(doc)

                audio_file = audio_file_path(doc)
                # Compute Mel Frequency Cepstral Coefficient (MFCC)
                click.secho(audio_file, fg='cyan')

                audio_ts, sampling_rate = librosa.load(audio_file)
                key = filename_without_extension(os.path.basename(doc))
                rms = librosa.feature.rmse(
                    y=audio_ts,
                    n_fft=2048,
                    hop_length=512
                )

                features[key] = rms[0]  # librosa.feature.rmse returns a list containing 1 list

                # Delete audio file
                self.remove_audio_file(doc)

        click.secho('Resampling energy vectors...', fg='cyan')
        # We need to resample the energy vector
        sampling_size = min([len(values) for values in features.values()])

        for key, value in features.items():
            features[key] = np.random.choice(value, sampling_size)

        click.secho('Saving energy vectors to dataframe...', fg='cyan')
        df = pd.DataFrame(features)
        df = df.transpose()
        df.columns = ['rmse_{}'.format(i + 1) for i in range(len(df.columns))]
        df.to_csv(os.path.join(self.output_path, 'signal_features_df.csv'))
