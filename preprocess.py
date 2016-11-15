#from preprocessing.shots_xml import ShotsProcessorXML
from preprocessing.shots_jpg import ShotsProcessorJPG
#from preprocessing.trans import TransProcessor


# processor = MetadataProcessor()
# processor.run()

# processor = ShotsProcessorXML()
# processor.run()

processor = ShotsProcessorJPG()
processor.run()

# processor = TransProcessor()
# processor.run()
