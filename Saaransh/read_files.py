import os
import PyPDF2
import docx2txt
import re
from werkzeug.utils import secure_filename

def read_txt(file_folder, filename):
    path=os.path.join(file_folder,filename)
    f=open(path,'r',encoding='utf-8',errors='ignore')
    res=f.read()
    f.close()

    os.remove(path)

    extracted_file_name=secure_filename('out1.txt')
    extracted_file_path=os.path.join(file_folder,extracted_file_name)
    exf=open(extracted_file_path,'w+',encoding='utf-8',errors='ignore')
    exf.write(res)
    exf.close()
    n=get_total_sentences(res)
    return n

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

    extracted_file_name=secure_filename('out1.txt')
    extracted_file_path=os.path.join(file_folder,extracted_file_name)
    exf=open(extracted_file_path,'w+',encoding='utf-8',errors='ignore')
    exf.write(text)
    exf.close()
    n=get_total_sentences(text)
    return n

def read_docx(file_folder, filename):
    path=os.path.join(file_folder,filename)
    res=docx2txt.process(path)
    extracted_file_name=secure_filename('out1.txt')
    extracted_file_path=os.path.join(file_folder,extracted_file_name)
    exf=open(extracted_file_path,'w+',encoding='utf-8',errors='ignore')
    exf.write(res)
    exf.close()

    os.remove(path)

    n=get_total_sentences(res)
    return n

def get_total_sentences(self):
    s=re.split('\.|\?|\!',self)
    return len(s)-1