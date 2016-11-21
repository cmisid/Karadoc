# from preprocessing.metadata import MetadataProcessor
# from preprocessing.trans import TransProcessor
# from preprocessing.shots import ShotsProcessor
from preprocessing.audio import SignalProcessor


# processor = MetadataProcessor()
# processor.run()

# processor = TransProcessor()
# processor.run()

# processor = ShotsProcessor()
# processor.run()

processor = SignalProcessor()
processor.run()
