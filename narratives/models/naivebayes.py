from sklearn.naive_bayes import MultinomialNB

def naivebayes(x, y):
    nb = MultinomialNB()
    return nb.fit(x, y)

