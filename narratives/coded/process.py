from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stopWords = set(stopwords.words('english'))

def remove_stopwords(string):
    words = word_tokenize(string)
    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)

    return ' '.join(wordsFiltered)

def process(df, segment):
    df[segment + "_swr"] = remove_stopwords(df[segment])
    return df
