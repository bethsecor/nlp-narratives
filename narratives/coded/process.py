from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
stopWords = set(stopwords.words('english'))

def remove_stopwords(stringList):
    removedStopWords = []
    for string in stringList:
        words = word_tokenize(string)
        wordsFiltered = []
        
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w)

        removedStopWords.append(' '.join(wordsFiltered))
    return removedStopWords


def process(df, segment):
    df[segment + "_swr"] = remove_stopwords(df[segment])
    return df
