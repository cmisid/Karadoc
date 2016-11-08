
import re

with open('data/tags.txt', 'r') as f:
    f.seek(100)
    content = f.read()

blocs = content.split('\n' * 2)

categories = []

for bloc in blocs:
    tag_regex = re.compile(r'\w+\/(\d)+')
    tag = tag_regex.search(bloc).group()[-4:]
    categories.append(tag)
