import os
import PyPDF2
import docx2txt
from sklearn.externals import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

def read_txt(file_folder, filename):
    path=os.path.join(file_folder,filename)
    f=open(path,'r',encoding='utf-8',errors='ignore')
    res=f.read()
    f.close()
    os.remove(path)

    return save_pkl(file_folder,res)

def read_pdf(file_folder, filename):
    path=os.path.join(file_folder,filename)
    pdfFileObj=open(path,'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
    num_pages=pdfReader.numPages
    count=0
    text=''
    while count<num_pages :
        pageObj=pdfReader.getPage(count)
        count+=1
        text+=pageObj.extractText()
    pdfFileObj.close()
    os.remove(path)

    return save_pkl(file_folder,text)

def read_docx(file_folder, filename):
    path=os.path.join(file_folder,filename)
    res=docx2txt.process(path)
    os.remove(path)

    return save_pkl(file_folder,res)

def save_pkl(file_folder,text):

    sent_list=sent_tokenize(text)
    i=len(sent_list)-1

    while(i>=0):
        if(len(sent_list[i].split())<3):
            del sent_list[i]
        i-=1

    n = len(sent_list)

    for i in range(n):
        if (i == 0):
            sent_list[i] = sent_list[i].replace(u'\ufeff', '')
        sent_list[i] = " ".join(sent_list[i].split())

    stop_words = set(stopwords.words('english'))
    lemma = nltk.wordnet.WordNetLemmatizer()

    docs = sent_list.copy()
    for i in range(n):
        sentence = ''
        for w in docs[i].split():
            if w not in stop_words:
                sentence += lemma.lemmatize(w) + ' '
        docs[i] = sentence

    sent_path=os.path.join(file_folder,'sent_list.pkl')
    joblib.dump(sent_list,sent_path)

    docs_path=os.path.join(file_folder,'docs_list.pkl')
    joblib.dump(docs,docs_path)

    vectorizer = TfidfVectorizer()
    A = vectorizer.fit_transform(docs)

    A_TFIDF_path=os.path.join(file_folder,'A_TFIDF.pkl')
    joblib.dump(A,A_TFIDF_path)

    return n
