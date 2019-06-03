from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

cv = CountVectorizer(lowercase=False)
tfidf = TfidfTransformer()

def extract_count(processed_variable):
    return cv.fit_transform(processed_variable)

def extract_tfidf(processed_variable):
    return tfidf.fit_transform(processed_variable)
