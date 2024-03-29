import os
import random
import string


from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload/files'
ALLOWED_EXTENSIONS = {'jpg', 'pdf', 'png', 'doc', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return render_template('index.html')

def random_generator():
    chars=string.ascii_uppercase+string.ascii_lowercase+string.digits
    return ''.join(random.choice(chars) for x in range(10))

@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        file_val = request.files['file']
        fname, file_extension = os.path.splitext(file_val.filename)
        fname=random_generator()
        newfile_name=fname+file_extension
        newFile = secure_filename(newfile_name)
        file_val.save(os.path.join(app.config['UPLOAD_FOLDER'], newFile))

        data=dict()
        data['fname']=newFile
        data['ctype']=file_val.content_type
        return jsonify(data)

@app.route('/predict')
def predict():
    n1 = request.values['n1']
    n2 = request.values['n2']
    data = dict()
    data['ans'] = n1 + n2
    return jsonify(data)


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(port=5000, debug=True)
