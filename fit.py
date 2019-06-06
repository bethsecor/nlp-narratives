from narratives.models.extract import extract_count, extract_tfidf
from collections import Counter
import feather

data = feather.read_dataframe('./data/coded_data.feather')

all_vars = data.columns.tolist()
x_vars = ['segment', 'segment_swr', 'segment_stem', 'segment_lemm']
y_vars = [e for e in all_vars if e not in x_vars + ['dataset']]

y_vars_10 = [var for var in y_vars if Counter(data[var])[1] >= 10]

print('Number of codes with 10 or more occurences: ' + str(len(y_vars_10)))

data = data[x_vars + y_vars_10 + ['dataset']]

for x in x_vars:
    data[x + '_cnt'] = extract_count(data[x])
    data[x + '_tfidf'] = extract_tfidf(data[x])

train = data[data.dataset == 'TRAIN']
test = data[data.dataset == 'TEST']

x_vars_ext = ['segment_cnt','segment_tfidf','segment_swr_cnt','segment_swr_tfidf','segment_stem_cnt','segment_lemm_cnt','segment_lemm_tfidf']

