from narratives.coded.parse import parse_atlas_output
from narratives.coded.convert import convert_doc2docx
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
uniq_segment = numpy.unique(data['segment'])
data_uniq = pandas.DataFrame({'uniq_segment': uniq_segment, 
                              'dataset': choice(['TRAIN','TEST'],len(uniq_segment),p=(0.7, 0.3))})
merge_data = data.merge(data_uniq, how='left', left_on='segment', right_on='uniq_segment')
final_data = merge_data.drop(columns=['uniq_segment'])
print(Counter(final_data['dataset']))

feather.write_dataframe(final_data, './data/coded_data.feather')
