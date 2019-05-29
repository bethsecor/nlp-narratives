from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
porter=PorterStemmer()
stopWords = set(stopwords.words('english'))

def process_segments(stringList, function):
    processedList = []
    for string in stringList:
        words = word_tokenize(string)
        wordsProcessed = []

        for w in words:
            if function == "stem":
                wordsProcessed.append(porter.stem(w))
            elif function == "stopwords":
                if w not in stopWords:
                    wordsProcessed.append(w)

        processedList.append(' '.join(wordsProcessed))
    return processedList


def process(df, segment):
    df[segment + "_swr"] = process_segments(df[segment], "stopwords")
    df[segment + "_swr_stem"] = process_segments(df[segment + "_swr"], "stem")

    return df
