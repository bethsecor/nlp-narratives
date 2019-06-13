import feather
from collections import Counter
from narratives.models.logistic import logistic
from narratives.models.naivebayes import naivebayes
from narratives.models.supportvector import supportvector
from sklearn.metrics import cohen_kappa_score, accuracy_score
import joblib
import pandas

data = feather.read_dataframe('./data/coded_data.feather')

all_vars = data.columns.tolist()
x_vars = ['segment', 'segment_swr', 'segment_stem', 'segment_lemm']
y_vars = [e for e in all_vars if e not in x_vars + ['dataset']]

y_vars_10 = [var for var in y_vars if Counter(data[var])[1] >= 10]

print('Number of codes with 10 or more occurences: ' + str(len(y_vars_10)))

data = data[x_vars + y_vars_10 + ['dataset']]
train = data[data.dataset == 'TRAIN']
test = data[data.dataset == 'TEST']

model_evaluation = pandas.DataFrame({'code':[],'x':[],'method':[],'dataset':[],'accuracy':[],'cohen_kappa':[]})
for code in ['Communication']:
#    for x in x_vars:
    x = 'segment'
    lr = logistic(train, code, x)
    joblib.dump(lr, './models/' + code.replace(' ', '\ ').replace('/', '-') + '.joblib')
    lr_pred_train = lr.predict(train[x])
    model_evaluation = model_evaluation.append(pandas.DataFrame({'code':[code],'x':[x],'method':['logistic'],'dataset':['train'],
                            'accuracy':[accuracy_score(train[code], lr_pred_train)],
                            'cohen_kappa':[cohen_kappa_score(train[code], lr_pred_train)]}))
    lr_pred_test = lr.predict(test[x])
    model_evaluation = model_evaluation.append(pandas.DataFrame({'code':[code],'x':[x],'method':['logistic'],'dataset':['test'],
                            'accuracy':[accuracy_score(test[code], lr_pred_test)],
                            'cohen_kappa':[cohen_kappa_score(test[code], lr_pred_test)]}))
#       nb = naivebayes(train, code, x)
#       print(nb)
#       svm = supportvector(train, code, x)
#       print(svm)

print(model_evaluation)
model_evaluation.to_csv('./models/model_evaluation.csv')
