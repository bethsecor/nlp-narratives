from sklearn.svm import SVC

def supportvector(x, y):
    svc = SVC(gamma='auto')
    return svc.fit(x, y)
