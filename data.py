from narratives.coded.parse import parse_atlas_output
from narratives.coded.convert import convert_doc2docx
from glob import glob
from pandas import pandas

frames = []
for doc in glob('./data/*.doc'):
    convert_doc2docx(doc, './data/')
    frames.append(parse_atlas_output(doc + "x"))

data = pandas.concat(frames)
print(data)
