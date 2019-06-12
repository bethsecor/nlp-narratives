from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def logistic(data, code, x):
    model = Pipeline([('cntvec', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', LogisticRegression(penalty="l2", solver="liblinear", multi_class="auto"))])
    return model.fit(data[x], data[code])
