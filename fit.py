import feather
from collections import Counter
from narratives.models.logistic import logistic
from narratives.models.naivebayes import naivebayes
from narratives.models.supportvector import supportvector
import joblib

data = feather.read_dataframe('./data/coded_data.feather')

all_vars = data.columns.tolist()
x_vars = ['segment', 'segment_swr', 'segment_stem', 'segment_lemm']
y_vars = [e for e in all_vars if e not in x_vars + ['dataset']]

y_vars_10 = [var for var in y_vars if Counter(data[var])[1] >= 10]

print('Number of codes with 10 or more occurences: ' + str(len(y_vars_10)))

data = data[x_vars + y_vars_10 + ['dataset']]
train = data[data.dataset == 'TRAIN']
test = data[data.dataset == 'TEST']

for code in y_vars_10:
#    for x in x_vars:
    lr = logistic(train, code, 'segment')
    joblib.dump(lr, './models/' + code.replace(' ', '\ ').replace('/', '-') + '.joblib')
#       nb = naivebayes(train, code, x)
#       print(nb)
#       svm = supportvector(train, code, x)
#       print(svm)
