import os
import string
import random
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,jsonify

UPLOAD_FOLDER = './upload/files'
EXTRACT_FILE ='upload/extracted.txt'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FILE'] = EXTRACT_FILE


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

def read_txt(file):
    f=open(file,'r')
    res=f.read()
    f.close()
    exf=open('./extracted.txt','w+')
    exf.write(res)
    exf.close()
    return True

def read_pdf(file):

    return ''

def read_doc(file):

    return ''


@app.route('/uploadajax', methods=['POST'])
def upldfile():
    data=dict()
    if request.method == 'POST':
        file_val = request.files['file']
        fname, file_extension = os.path.splitext(file_val.filename)
        fname=random_generator()
        newfile_name=fname+file_extension
        newfilename = secure_filename(newfile_name)
        new_path=os.path.join(app.config['UPLOAD_FOLDER'], newfilename)
        file_val.save(new_path)

        if os.path.exists(new_path):
            data['result']=newfilename
            data['status']='200'
            if(file_extension=='txt'):
                read_txt(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
            elif(file_extension=='pdf'):
                content="pdf file uploaded"
            elif(file_extension=='doc'):
                content="doc uploaded"
            else:
                content="docx uploaded"

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
    exf=open('./extracted.txt','r')
    content=exf.read()
    req['summary']=content
    return jsonify(req)


if __name__=='__main__':
    app.run(port=8000,debug=True)