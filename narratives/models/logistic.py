from sklearn.linear_model import LogisticRegression

def logistic(x, y):
    lr = LogisticRegression()
    return lr.fit(x, y)
