import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
englishSnowballStemmer = SnowballStemmer("english", ignore_stopwords=True)
stopWords = set(stopwords.words('english'))
wordNetLemma = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def process_segments(stringList, function):
    processedList = []
    for string in stringList:
        words = word_tokenize(string)
        wordsProcessed = []

        for w in words:
            if function == "stem":
                wordsProcessed.append(englishSnowballStemmer.stem(w.lower()))            
            elif function == "lemmatize":
                wordsProcessed.append(wordNetLemma.lemmatize(w, get_wordnet_pos(w)))
            elif function == "stopwords":
                if w not in stopWords:
                    wordsProcessed.append(w.lower())
        
        processedList.append(' '.join(wordsProcessed))
    return processedList


def process(df, segment):
    df[segment + "_swr"] = process_segments(df[segment], "stopwords")
    df[segment + "_stem"] = process_segments(df[segment], "stem")
    df[segment + "_lemm"] = process_segments(df[segment + "_swr"], "lemmatize")
    return df
