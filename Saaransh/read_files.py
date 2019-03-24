import os
import PyPDF2
import docx2txt
from werkzeug.utils import secure_filename


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
