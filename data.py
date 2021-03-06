from narratives.coded.parse import parse_atlas_output
from narratives.coded.convert import convert_doc2docx
from narratives.coded.transform import transform
from narratives.coded.process import process
from glob import glob
from pandas import pandas
import numpy
from numpy.random import choice
from collections import Counter
import feather

frames = []
for doc in glob('./data/*.doc'):
    convert_doc2docx(doc, './data/')
    frames.append(parse_atlas_output(doc + "x"))

data = pandas.concat(frames)
transformed_data = transform(data, 'code')
transformed_data['dataset'] = choice(['TRAIN','TEST'], len(transformed_data['segment']), p=(0.7, 0.3))
print(Counter(transformed_data['dataset']))

processed_data = process(transformed_data, 'segment')
print(processed_data)

feather.write_dataframe(processed_data, './data/coded_data.feather')
