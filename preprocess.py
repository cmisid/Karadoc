import pandas as pd

from preprocessing.metadata import MetadataProcessor


processor = MetadataProcessor('data/metadata/')
features = processor.run()
features.to_csv('tfidf.csv')
