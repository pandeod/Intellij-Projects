import os
import random
import shutil
import string
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from read_files import read_txt, read_docx, read_pdf
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
    return render_template('index.html')


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

    if(len(docs)>1):
        k=app.config['k']
        GRS_sen = get_grs_score(file_folder,k)
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

        summary_final = ''

        for i in range(n):
            if total_score[i] in top_list:
                summary_final += sent_list[i] + '\n'

        return summary_final
    else:
        return 'No meaningful sentence found'


@app.route('/uploadajax', methods=['POST'])
def upldfile():
    data = dict()
    if request.method == 'POST':
        file_val = request.files['file']
        fname, file_extension = os.path.splitext(file_val.filename)
        file_folder = random_generator() + '/'

        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_folder)
        directory = os.path.dirname(new_file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        newfile_name = 'input' + file_extension
        newfilename = secure_filename(newfile_name)
        new_path = os.path.join(directory, newfilename)
        file_val.save(new_path)

        if os.path.exists(new_path):
            if (file_extension == '.txt'):
                res = read_txt(directory, newfilename)
            elif (file_extension == '.pdf'):
                res = read_pdf(directory, newfilename)
            else:
                res = read_docx(directory, newfilename)

            length=res[0]
            app.config['k']=res[1]
            data['result'] = file_folder
            data['length'] = length
            data['status'] = '200'
            return jsonify(data)
        else:
            data['result'] = "No File Uploaded"
            data['status'] = '404'
            data['length'] = '0'
            return jsonify(data)
    else:
        data['result'] = "Error In Request"
        data['statusFile'] = '405'
        return jsonify(data)


@app.route('/requestsummary', methods=['POST'])
def requestsummary():
    start=timer()
    req = dict()
    folder_str = request.json['fname']
    sumLen = request.json['sumLen']

    logging.warning(sumLen)

    file_folder = app.config['UPLOAD_FOLDER']+folder_str
    sents = summary_nmf_method(file_folder, sumLen)

    t=timer()-start

    sents="Time required : "+str(t)+" seconds. \n"+sents
    req['summary'] = sents
    return jsonify(req)


@app.route('/getfile', methods=['POST'])
def getfile():
    folder = request.get_data()
    folder_str = folder.decode('utf-8')
    file_folder = folder_str + 'out1.txt'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_folder)
    try:
        return send_file(file_path, attachment_filename='out1.txt', as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/closesummary', methods=['POST'])
def closesummary():
    req = dict()
    folder = request.get_data()
    folder_str = folder.decode('utf-8')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_str)
    shutil.rmtree(file_path, True)
    req['response'] = 'success'
    req['status'] = '200'
    return jsonify(req)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
