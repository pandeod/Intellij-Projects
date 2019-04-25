from sklearn.decomposition import NMF
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import os
import gensim
from itertools import combinations


def get_descriptor( all_terms, H, topic_index, top ):
    # reverse sort the values to sort the indices
    top_indices = np.argsort( H[topic_index,:] )[::-1]
    # now get the terms corresponding to the top-ranked indices
    top_terms = []
    for term_index in top_indices[0:top]:
        top_terms.append( all_terms[term_index] )
    return top_terms

def calculate_coherence( w2v_model, term_rankings ):
    overall_coherence = 0.0
    for topic_index in range(len(term_rankings)):
        # check each pair of terms
        pair_scores = []
        for pair in combinations( term_rankings[topic_index], 2 ):
            try:
                pair_scores.append( w2v_model.similarity(pair[0], pair[1]) )
            except Exception as e:
                pair_scores.append(0)
        # get the mean for all pairs in this topic
        topic_score = sum(pair_scores) / len(pair_scores)
        overall_coherence += topic_score
    # get the mean score across all topics
    return overall_coherence / len(term_rankings)

def select_k_component(file_folder):
    kmin, kmax = 4, 15

    A_TFIDF_path=os.path.join(file_folder,'A_TFIDF.pkl')
    (A,terms)=joblib.load(A_TFIDF_path)

    topic_models = []
    # try each value of k
    for k in range(kmin,kmax+1):
        print("Applying NMF for k=%d ..." % k )
        # run NMF
        model = NMF(init="nndsvd", n_components=k)
        W = model.fit_transform(A)
        H = model.components_
        # store for later
        topic_models.append((k,W,H))

    w2v_model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True,limit=500000)

    k_values = []
    coherences = []
    for (k,W,H) in topic_models:
        # Get all of the topic descriptors - the term_rankings, based on top 10 terms
        term_rankings = []
        for topic_index in range(k):
            term_rankings.append( get_descriptor( terms, H, topic_index, 10 ) )
        # Now calculate the coherence based on our Word2vec model
        k_values.append( k )
        coherences.append( calculate_coherence( w2v_model, term_rankings ) )
        print("K=%02d: Coherence=%.4f" % ( k, coherences[-1] ) )

    return k_values[coherences.index(max(coherences))]



