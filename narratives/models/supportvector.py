from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

def supportvector(data, code, x):
    model = Pipeline([('cntvec', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', SVC(gamma="auto"))])
    return model.fit(data[x], data[code])

