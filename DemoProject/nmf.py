from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
import pandas as pd
import numpy as np

def weight_H_i(i,H_col,summation_H,H):
    sum_H_col=0
    for j in range(H_col):
        sum_H_col+=H[i][j]
    w_H_i=sum_H_col/summation_H
    return w_H_i

def grs_sent_j(j,H_row,H_col,summation_H,H):
    sum_score=0
    for i in range(H_row):
        sum_score+=H[i][j]*weight_H_i(i,H_col,summation_H,H)
    return sum_score

def get_grs_score(docs):
    vec = CountVectorizer()
    X = vec.fit_transform(docs)
    df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    A_t=df.values
    A=np.transpose(A_t)

    model = NMF(init='random',n_components=25, random_state=0)
    W = model.fit_transform(A)
    H = model.components_

    H_row=len(H)
    H_col=len(H[0])
    summation_H=0

    for i in range(H_row):
        for j in range(H_col):
            summation_H+=H[i][j]

    GRS_sen=list()

    for j in range(H_col):
        GRS_sen.append(grs_sent_j(j,H_row,H_col,summation_H,H))

    return GRS_sen
