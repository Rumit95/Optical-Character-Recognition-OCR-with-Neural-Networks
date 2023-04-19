import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from keras.models import load_model
#import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from PIL import Image
import pickle

#label=pd.read_csv("labels.csv",header=2)

UPLOAD_FOLDER = 'C:/Users/Rumit/Downloads/Git/English Printed/Static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
s = pickle.load( open("Classes.pkl",'rb'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = load_model('Model2.hdf5')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def multi(img1):
    img1 = img_to_array(img1)
    #na = (255-img)
    na = img1/255
    na = na.reshape(1,64 ,64,1 )
    temp = model.predict(na)
    temp = np.argmax(temp)
    return  s[s.values==temp].index[0].split('-')[-1]
    
    

def predict(img2):
    #img = load_img(filename)
    #img = img.convert('L')
    arr=img_to_array(img2).reshape(img_to_array(img2).shape[0], img_to_array(img2).shape[1])
    li=[]
    ind=[]
    for col in range(arr.shape[1]):
        #print(col)
        li.append(arr[:,col])
        #print(li[0])
        if np.mean(li[0])>=245:
            ind.append(col)
        li=[]
    b=[]
    for i in ind:   
        if i+1 not in ind or i-1 in ind:
            b.append(i)
        loc=[]
    bla=0
    for sp in range(len(b)-1):
        if b[sp+1]-b[sp]>30:
            loc.append(bla)
        bla=bla+1
    #print(loc)
    new=[]
    coun=0
    for ps in range(len(loc)-1):
        if loc[ps+1]-loc[ps]>20:
            new.append(coun)
        coun=coun+1
    final=np.split(arr, b, axis=1)
    c=0
    emp=[]
    for i in final:
        
        if c==0 or c==len(final)-1:
            pass
        elif i.shape[1]>10:
        #print(i.shape)
            #plt.imshow(i)
            #plt.show()
            img2 = Image.fromarray(i)
            #img.save(c,'.png')
            #img=img.resize(32,32)
            #print(type(i))
            #plt.imshow(img.resize([32,32]))
            emp.append(multi(img2.resize([64,64])))
        c=c+1
    for k in new:
        emp.insert(k+1," ")
    return emp

def para(filename):
    img = load_img(filename)
    #img = load_img('Static/sample.png')
    img = img.convert('L')
    arr1=img_to_array(img).reshape(img_to_array(img).shape[0], img_to_array(img).shape[1])
    #print(arr1.shape)
    ri=[]
    rw=[]
    for row in range(arr1.shape[0]):
        #print(row)
        ri.append(arr1[row,:])
        #print(ri[0])
        if np.mean(ri[0])>=250:
            rw.append(row)
        ri=[]
    d=[]
    for i in rw:   
        if i+1 not in rw or i-1 in rw:
            d.append(i)
    final1=np.split(arr1, d, axis=0)
    g=0
    an=[]
    for i in final1:
        if g==0 or g==len(final1)-1:
            pass
        elif i.shape[1]>10:
            #print(i.shape)
            img = Image.fromarray(i)
            #plt.imshow(img)
            #plt.show()
            an.append(predict(img))
        g=g+1
    #plt.show()
    r=[]
    for i in an:
        r.append("".join(i))
    ans1=" ".join(r)
    return ans1


@app.route('/')
def home():
        return render_template("home.html")

@app.route('/result', methods=['GET', 'POST'])
def upload_file():
    error=''
    target=UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.save(os.path.join(target, file.filename))
            img_path=os.path.join(target, file.filename)
            img=file.filename
            li=para(img_path)
            #li1=[]
            #for i in li[0]:
                 #li1.append("{0:.3f}".format(i))
            return render_template('result.html',img=img,prob=li)
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug = True)