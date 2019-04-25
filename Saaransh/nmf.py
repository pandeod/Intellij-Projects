from sklearn.decomposition import NMF
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import os
from parameter_selection_nmf import select_k_component

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

def get_grs_score(file_folder):
    k=select_k_component(file_folder)

    A_TFIDF_path=os.path.join(file_folder,'A_TFIDF.pkl')
    (A_t,terms)=joblib.load(A_TFIDF_path)
    A=np.transpose(A_t)

    model = NMF(init='random',n_components=k, random_state=0)
    W = model.fit_transform(A)
    H = model.components_

    H_row=len(H)
    H_col=len(H[0])
    summation_H=0

    for i in range(H_row):
        for j in range(H_col):
            summation_H+=H[i][j]

    g=list()

    for j in range(H_col):
        g.append(grs_sent_j(j,H_row,H_col,summation_H,H))

    GRS_sen=np.array(g)
    maxGRS=GRS_sen.max()
    GRS_sen=(100*GRS_sen)/maxGRS

    return GRS_sen
