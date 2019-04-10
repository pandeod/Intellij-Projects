import logging
import numpy as np
from nltk.cluster.util import cosine_distance

np.seterr(divide='ignore', invalid='ignore')

def sentence_similarity(s1, s2):
    sent1=s1.split()
    sent2=s2.split()
    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        vector2[all_words.index(w)] += 1
    with np.errstate(divide='ignore',invalid='ignore'):
        return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences):
    # Create an empty similarity matrix
    S = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            S[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2])

    # normalize the matrix row-wise
    for idx in range(len(S)):
        row_sum=S[idx].sum()
        if(row_sum!=0):
            S[idx] /= row_sum

    return S

def pagerank(docs, eps=0.0001, d=0.85):
    A=build_similarity_matrix(docs)

    logging.warning('Matrix Build Complete')

    P = np.ones(len(A)) / len(A)
    while True:
        new_P = np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P