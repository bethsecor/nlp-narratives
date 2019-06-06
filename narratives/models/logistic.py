from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def logistic(code, x_vars_ext):
    for x in x_vars_ext:
        lr = LogisticRegression()
        lr.fit(train[x], code)
   # add cross validation here and output best model based on metric 
