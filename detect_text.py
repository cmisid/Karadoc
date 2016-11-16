import pytesseract
from PIL import Image

image_path = 'data/shots/Anglicantv-FCA2009ArchbishopVenables921/00371.jpg'

text = pytesseract.image_to_string(Image.open(image_path))
print(text)
