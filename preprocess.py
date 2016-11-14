from preprocessing.metadata import MetadataProcessor
from preprocessing.shots import ShotsProcessor
from preprocessing.trans import TransProcessor


# processor = MetadataProcessor()
# processor.run()

# processor = ShotsProcessor()
# processor.run()

processor = TransProcessor()
processor.run()
