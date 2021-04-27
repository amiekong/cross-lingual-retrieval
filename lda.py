from stemmer import PorterStemmer
import string
import re
from nltk.stem import *
import nltk
import itertools
from gensim import corpora, models
import gensim
from sklearn.decomposition import LatentDirichletAllocation as LDA
from tqdm import tqdm
import en_core_web_sm


#Retrieves stop words from stoplist.txt file
def get_stopwords():
    stop_words = [word for word in open('stoplist.txt','r').read().split('\n')]
    return stop_words

#Stems words using PorterStemmer implemented in stemmer.py
def stem_words(tokens):
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(token) for token in tokens]
    return stemmed_words

#Removes stop words taken from stoplist.txt
def remove_stop_words(tokens):
    stop_words = get_stopwords()
    filtered_words = [token for token in tokens if token not in stop_words and len(token) > 2]
    return filtered_words


#Tokenizes given string and removes punctuation.
def tokenize_and_remove_punct(aString):
    toString = str.maketrans('','',string.punctuation)
    token = aString.translate(toString)
    token = ''.join([i for i in token if not i.isdigit()])
    #return nltk.word_tokenize(token)
    return token.split()

def preprocess_data(data):
    dataDict = {}
    for text in data:
        tokens = tokenize_and_remove_punct(text[1])
        filtered_tokens = remove_stop_words(tokens)
        stemmed_tokens = stem_words(filtered_tokens)
        filtered_tokens1 = remove_stop_words(stemmed_tokens)
        dataDict[text[0]] = filtered_tokens1
    return dataDict

def tokenization_with_gen_stop(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(token)

    return result


def get_topics(final):
    final_preprocess = preprocess_data(final)
    #topic modeling on results list of top 10
    nlp = en_core_web_sm.load()

    data_lemma = []

    for txt in tqdm(final_preprocess):
        lis = []
        doc = nlp(txt)
        for token in doc:
            lis.append(token.lemma_)
        data_lemma.append(' '.join(lis))

    data_words = []

    for txt in tqdm(data_lemma):
        data_words.append(tokenization_with_gen_stop(txt))

    data_words_clean = []

    for word in tqdm(data_words):
        wrd = []
        for w in word:
            wrd.append(w)
        data_words_clean.append(wrd)

    dictionary = corpora.Dictionary(data_words_clean)
    dictionary.filter_extremes(no_below=3)
    corpus = [dictionary.doc2bow(text) for text in data_words_clean]

    lda_model = models.LdaModel(corpus, num_topics=5, \
                                 id2word=dictionary, \
                                  passes=5, alpha=[0.01]*5, \
                                  eta=[0.01]*len(dictionary.keys()))

    new_query = ""
    for i, topic in sorted(lda_model.show_topics(formatted=True, num_topics=2, num_words=1)):
        new_query = new_query + str(topic)

    return new_query
