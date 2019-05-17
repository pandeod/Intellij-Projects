import os
import random
import shutil
import string
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from read_files import read_txt, read_docx, read_pdf, save_pkl
from textrank import pagerank, sentence_similarity, build_similarity_matrix
from surface_feature import get_surface_score
from nmf import get_grs_score
from rank_sentences import get_top_list
from lexrank import STOPWORDS, LexRank
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import logging
import json

from sklearn.externals import joblib

from timeit import default_timer as timer


# nltk.download('stopwords')
# nltk.download('wordnet')

UPLOAD_FOLDER = './upload/files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def root():
    f_dir='files/'
    f_input='a.txt'
    sumLen=10
    fname, file_extension = os.path.splitext(f_input)
    file_folder = './upload/files/'

    file_path=os.path.join(f_dir,f_input)

    if (file_extension == '.txt'):
        res = read_txt(file_path)
    elif (file_extension == '.pdf'):
        res = read_pdf(file_path)
    else:
        res = read_docx(file_path)

    return summary_nmf_method(file_folder,sumLen)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def random_generator():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(10))


def split_file_name(filename):
    upload_file = dict()
    fname, file_extension = os.path.splitext(filename)
    upload_file['fname'] = fname
    upload_file['file_extension'] = file_extension
    return jsonify(upload_file)

def summary_nmf_method(file_folder,sumLen):

    sent_path=os.path.join(file_folder,'sent_list.pkl')
    sent_list=joblib.load(sent_path)

    docs_path=os.path.join(file_folder,'docs_list.pkl')
    docs=joblib.load(docs_path)

    n = len(sent_list)

    if(n>1):
        GRS_sen = get_grs_score(file_folder)
        surface_score = get_surface_score(docs)
        # p=pagerank(docs)

        lxr = LexRank(docs)
        lx = lxr.rank_sentences(docs, threshold=None, fast_power_method=True)

        lxr_score = np.array(lx)
        maxLex = lxr_score.max()
        lxr_score = (100 * lxr_score) / maxLex

        total_score = []

        for i in range(n):
            t_sum = float(GRS_sen[i]) + float(surface_score[i]) + float(lxr_score[i])
            total_score.append(t_sum)

        copy_score = total_score.copy()
        top_list = get_top_list(copy_score, sumLen)

        summary_final = '<h3>Total Sentecnes :' + str(len(total_score)) + '</h3>'
        summary_final+='<h3>Selected Sentecnes :' + str(sumLen) + '</h3>'

        for i in range(n):
            if (total_score[i] in top_list):
                summary_final += '<p style="color:#00ff00">' + sent_list[i] +'<br>'+str(total_score[i])+ '</p>'
            else:
                summary_final += '<p style="color:#ff0000">' + sent_list[i] +'<br>'+str(total_score[i])+ '</p>'

        os.remove(sent_path)
        os.remove(docs_path)

        return summary_final
    elif(n==1):
        os.remove(sent_path)
        os.remove(docs_path)

        return sent_list[0]
    else:
        os.remove(sent_path)
        os.remove(docs_path)

        return 'No adequate sentences found for summary.'

if __name__ == '__main__':
    app.run(port=8000, debug=True)
