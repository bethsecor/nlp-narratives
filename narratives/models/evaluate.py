from sklearn.metrics import cohen_kappa_score, classification_report

def evaluate(y, predicted):
    return cohen_kappa_score(y, predicted)
