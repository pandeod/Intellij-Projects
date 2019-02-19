import os
import random
import shutil
import string

import PyPDF2
import docx2txt
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload/files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def root():
    return render_template('index.html')

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_generator():
    chars=string.ascii_uppercase+string.ascii_lowercase+string.digits
    return ''.join(random.choice(chars) for x in range(10))

def split_file_name(filename):
    upload_file=dict()
    fname, file_extension = os.path.splitext(filename)
    upload_file['fname']=fname
    upload_file['file_extension']=file_extension
    return jsonify(upload_file)

def read_txt(file_folder, filename):
    path=os.path.join(file_folder,filename)
    f=open(path,'r')
    res=f.read()
    f.close()
    extracted_file_name=secure_filename('out1.txt')
    extracted_file_path=os.path.join(file_folder,extracted_file_name)
    exf=open(extracted_file_path,'w+')
    exf.write(res)
    exf.close()
    return res

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

    extracted_file_name=secure_filename('out1.txt')
    extracted_file_path=os.path.join(file_folder,extracted_file_name)
    exf=open(extracted_file_path,'w+')
    exf.write(text)
    exf.close()
    return text

def read_doc(file_folder, filename):
    # path=os.path.join(file_folder,filename)
    # res=docx2txt.process(path)
    # extracted_file_name=secure_filename('out1.txt')
    # extracted_file_path=os.path.join(file_folder,extracted_file_name)
    # exf=open(extracted_file_path,'w+')
    # exf.write(res)
    # exf.close()
    return True

def read_docx(file_folder, filename):
    path=os.path.join(file_folder,filename)
    res=docx2txt.process(path)
    extracted_file_name=secure_filename('out1.txt')
    extracted_file_path=os.path.join(file_folder,extracted_file_name)
    exf=open(extracted_file_path,'w+')
    exf.write(res)
    exf.close()
    return res


@app.route('/uploadajax', methods=['POST'])
def upldfile():
    data=dict()
    if request.method == 'POST':
        file_val = request.files['file']
        fname, file_extension = os.path.splitext(file_val.filename)
        file_folder=random_generator()+'/'

        new_file_path=os.path.join(app.config['UPLOAD_FOLDER'],file_folder)
        directory = os.path.dirname(new_file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if(file_extension=='.doc'):
            file_extension='.docx'

        newfile_name='input'+file_extension
        newfilename = secure_filename(newfile_name)
        new_path=os.path.join(directory, newfilename)
        file_val.save(new_path)

        if os.path.exists(new_path):
            if(file_extension=='.txt'):
                content=read_txt(directory, newfilename)
            elif(file_extension=='.pdf'):
                content=read_pdf(directory, newfilename)
            elif(file_extension=='.doc'):
                content=read_doc(directory, newfilename)
            else:
                content=read_docx(directory, newfilename)

            data['result']=file_folder
            data['status']='200'
            return jsonify(data)
        else:
            data['result']="No File Uploaded"
            data['status']='404'
            return jsonify(data)
    else :
        data['result']="Error In Request"
        data['statusFile']='405'
        return jsonify(data)

@app.route('/requestsummary', methods=['POST'])
def requestsummary():
    req=dict()
    folder=request.get_data()
    folder_str=folder.decode('utf-8')
    file_folder=folder_str+'out1.txt'
    file_path=os.path.join(app.config['UPLOAD_FOLDER'],file_folder)
    f=open(file_path,'r')
    content=f.read()
    f.close()
    req['summary']=content
    return jsonify(req)

@app.route('/closesummary', methods=['POST'])
def closesummary():
    req=dict()
    folder=request.get_data()
    folder_str=folder.decode('utf-8')
    file_path=os.path.join(app.config['UPLOAD_FOLDER'],folder_str)
    shutil.rmtree(file_path,True)
    req['response']='success'
    req['status']='200'
    return jsonify(req)

if __name__=='__main__':
    app.run(port=8000,debug=True)