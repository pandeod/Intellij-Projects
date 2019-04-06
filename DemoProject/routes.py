from flask import Flask, render_template, request, jsonify, send_file
from textrank import pagerank,sentence_similarity,build_similarity_matrix
from surface_feature import get_surface_score
from nmf import get_grs_score
from rank_sentences import get_top_list
from lexrank import STOPWORDS, LexRank
import re
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')
# nltk.download('wordnet')

app = Flask(__name__)

@app.route('/')
def root():
    f=open('files/a.txt','r',encoding='utf-8',errors='ignore')
    text=f.read()
    summary=summary_nmf_method(text)
    return ''+summary

def summary_nmf_method(text):

    lemma = nltk.wordnet.WordNetLemmatizer()
    sent_list=re.split('\.|\?|\!',text)
    sent_list.pop()
    docs=sent_list.copy()
    n=len(docs)

    for i in range(n):
        if(i==0):
            docs[i]=docs[i].replace(u'\ufeff','')
            sent_list[i]=sent_list[i].replace(u'\ufeff','')
        docs[i]=" ".join(docs[i].split()).lower()
        sent_list[i]=" ".join(sent_list[i].split())

    stop_words = set(stopwords.words('english'))

    for i in range(n):
        sentence=''
        for w in docs[i].split():
            if w not in stop_words:
                sentence+=lemma.lemmatize(w)+' '
        docs[i]=sentence

    GRS_sen=get_grs_score(docs)
    surface_score=get_surface_score(docs)
    p=pagerank(docs)
    lxr = LexRank(docs)

    scores_cont = lxr.rank_sentences(docs,threshold=None,fast_power_method=True)

    total_score=[]

    for i in range(n):
        t_sum=float(GRS_sen[i])+float(surface_score[i])+float(p[i])+float(scores_cont[i])
        total_score.append(t_sum)

    copy_score=total_score.copy()
    top_list=get_top_list(copy_score)

    #summary_final='<h3>Total Sentecnes :'+str(len(total_score))+'</h3>'+'<h3>Sentecnes Selected :'+str(len(top_list))+'</h3>'
    # i=0
    # while(i<n):
    #     if total_score[i] in top_list:
    #         summary_final+='<p>'+sent_list[i]+'&nbsp; &nbsp;'+str(total_score[i])+'</p>'
    #     else:
    #         summary_final+='<p>----- '+sent_list[i]+'&nbsp; &nbsp;'+str(total_score[i])+' -----</p>'
    #     i+=1

    summary_final='<h3>Total Sentecnes :'+str(len(total_score))+'</h3>'

    for i in range(n):
        if(total_score[i] in top_list):
            summary_final+='<p>'+sent_list[i]+'</p>'
        else:
            summary_final+='<p style="color:#ff0000">'+sent_list[i]+'</p>'

    return summary_final

if __name__=='__main__':
    app.run(port=8000,debug=True)