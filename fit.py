from narratives.models.extract import extract_count, extract_tfidf
from narratives.models.logistic import logistic
from narratives.models.naivebayes import naivebayes
from narratives.models.supportvector import supportvector
from narratives.models.evaluate import evaluate
from collections import Counter
import feather


data = feather.read_dataframe('./data/coded_data.feather')
# ignore any codes with less than 10 occurences
all_vars = data.columns.tolist()
x_vars = ['segment', 'segment_swr', 'segment_stem', 'segment_lemm']
y_vars = [e for e in all_vars if e not in x_vars + ['dataset']]

y_vars_10 = [var for var in y_vars if Counter(data[var])[1] >= 10]

print(len(y_vars))
print(len(y_vars_10))
