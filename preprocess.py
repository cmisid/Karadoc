import pandas as pd

from preprocessing.metadata import MetadataProcessor
from preprocessing.shots import ShotsProcessor


processor = MetadataProcessor()
processor.run()

# processor = ShotsProcessor()
# processor.run()
