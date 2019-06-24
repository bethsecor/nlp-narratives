import feather
from collections import Counter
from narratives.models.logistic import logistic
from narratives.models.naivebayes import naivebayes
from narratives.models.supportvector import supportvector
from sklearn.metrics import cohen_kappa_score, accuracy_score
from sklearn.utils import resample
import joblib
from pandas import DataFrame, concat
from numpy import argmax

data = feather.read_dataframe('./data/coded_data.feather')

all_vars = data.columns.tolist()
x_vars = ['segment', 'segment_swr', 'segment_stem', 'segment_lemm']
y_vars = [e for e in all_vars if e not in x_vars + ['dataset']]

y_vars_10 = [var for var in y_vars if Counter(data[var])[1] >= 10]

print('Number of codes with 10 or more occurences: ' + str(len(y_vars_10)))

data = data[x_vars + y_vars_10 + ['dataset']]
train = data[data.dataset == 'TRAIN']
test = data[data.dataset == 'TEST']

results = DataFrame({'code':[], 
                     'x':[],
                     'method':[],
                     'dataset':[],
                     'accuracy':[],
                     'kappa':[]})

for code in y_vars_10:
    print(code)

    majority = train[train[code] == 0]
    minority = train[train[code] == 1]

    minority_up = resample(minority,
                           replace=True,
                           n_samples=majority.shape[0],
                           random_state=428)

    train_upsampled = concat([majority, minority_up])

    models = []
    test_kappa = []

    for x in x_vars:
        lr = logistic(train_upsampled, code, x)
        
        lr_pred_train = lr.predict(train[x])
        lr_pred_test = lr.predict(test[x])

        train_results = DataFrame({'code':[code],
                                   'x':[x],
                                   'method':['logistic'],
                                   'dataset':['train'],
                                   'accuracy':[accuracy_score(train[code], 
                                                              lr_pred_train)],
                                   'kappa':[cohen_kappa_score(train[code], 
                                                              lr_pred_train)]
                                  })

        test_results = DataFrame({'code':[code],
                                  'x':[x],
                                  'method':['logistic'],
                                  'dataset':['test'],
                                  'accuracy':[accuracy_score(test[code], 
                                                             lr_pred_test)],
                                  'kappa':[cohen_kappa_score(test[code], 
                                                             lr_pred_test)]
                                 })

        results = results.append([train_results,
                                  test_results],
                                 sort=False)

        models.append(lr)
        test_kappa.append(cohen_kappa_score(test[code], lr_pred_test))

    joblib.dump(models[argmax(test_kappa)], './models/' + code + '.joblib')

print(results)
results.to_csv('./models/model_evaluation.csv')

