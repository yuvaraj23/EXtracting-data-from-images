from __future__ import division, print_function
import matplotlib.pyplot as plt
import os
import cv2
import pandas
import numpy
import re
from tr import *
from PIL import Image, ImageDraw, ImageFont
from dateutil.parser import parse



# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

a=[]
def find_date(texts):
    match = re.search(r'([\d]{1,2}[-|/|.](JAN|Jan|FEB|Feb|MAR|Mar|APR|Apr|April|MAY|May|JUN|Jun|JUL|Jul||AUG|Aug|SEP|Sep|OCT|Oct|NOV|Nov|DEC|Dec|[0-9]\d*)[-|/|.|][\d]{2,4})',texts)
    DATE=str(match)
    if(len(DATE)>5):
        #print("DATE IS PRESENT")
        #print(match[0])
        a.append(match[0])
    else:
        print("")
    try:
        return str(match[0])
    except:
        return str(match)
           
def find_date1(texts):
    match1 = re.findall(r'([\d]{2,4}[-|/|.](JAN|Jan|FEB|Feb|MAR|Mar|APR|April|Apr|MAY|May|JUN|Jun|June|JUL|Jul|AUG|Aug|SEP|Sep|OCT|Oct|NOV|Nov|DEC|Dec|[0-9]\d*)[-|/|.][\d]{1,2})',texts)
    for i in range(len(match1)):
        if(int(match1[i][0][0]) <= 2):
            if(len(match1[i])>1):
                #print("DATE IS PRESENT")
                #print(match1[i][0])
                a.append(match1[i][0])
    try:
        return str(match1[i][0])
    except:
        return str(match1)

    
def find_date2(texts):
    match2 = re.findall(r'([\d]{2,4}[-|/|.](JAN|Jan|FEB|Feb|MAR|Mar|APR|April|Apr|MAY|May|JUN|Jun|June|JUL|Jul|AUG|Aug|SEP|Sep|OCT|Oct|NOV|Nov|DEC|Dec|[0-9]\d*)[-|/|.][\d]{4})',texts)
    for i in range(len(match2)):
        if(int(match2[i][0][0]) <= 2):
            if(len(match2[i])>1):
                #print("DATE IS PRESENT")
                #print(match1[i][0])
                a.append(match2[i][0])
    try:
        return str(match2[i][0])
    except:
        return str(match2)
              
        
def find_date3(texts):
    match3= re.findall(r"((JAN|Jan|FEB|Feb|MAR|Mar|APR|Apr|April|MAY|May|JUN|June|Jun|JUL|Ju1|AUG|Aug|SEP|Sep|OCT|Oct|NOV|Nov|DEC|Dec)[\d]{1,2}[-|'|/|.|,][\d]{2,4})",texts)
    if(len(match3)==0):
        print("")
    elif(len(match3[0])>1):
        #print("DATE IS PRESENT")
        #print(match2[0][0])
        a.append(match3[0][0])
    try:
        return str(match3[0][0])
    except:
        return str(match3)
        
def find_date4(texts):
    match4 = re.search(r'([\d]{1,2}(JAN|Jan|FEB|Feb|MAR|Mar|APR|Apr|April|MAY|May|JUN|Jun|JUL|Jul|AUG|Aug|SEP|Sep|OCT|Oct|NOV|Nov|DEC|Dec)[\d]{2,4})',texts)
    DATE=str(match4)
    if(len(DATE)>5):
        #print("DATE IS PRESENT")
        #print(match3[0])
        a.append(match4[0])
    try:
        return str(match4[0])
    except:
        return str(match4)



def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def image_text(img,find_date,find_date1,find_date2,find_date3,find_date4, is_date):
    #data_folder= "/home/yuvaraj/Downloads/receipts/Receipts/"

    a=[]
 
    #img_pil = Image.open(data_folder+os.listdir(data_folder)[i])#6d53e280#6eef3a7f.jpeg#4e7babf5
    img_pil = Image.open(img)
    MAX_SIZE = 2000
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.BICUBIC)

    print(img_pil.width, img_pil.height)
    #img_pil
    gray_pil = img_pil.convert("L")

    rect_arr = detect(img_pil, FLAG_RECT)

    img_draw = ImageDraw.Draw(img_pil)
    colors = ['red', 'green', 'blue', "yellow", "pink"]

    for i, rect in enumerate(rect_arr):
        x, y, w, h = rect
        img_draw.rectangle((x, y, x + w, y + h),outline=colors[i % len(colors)])

    #img_pil
    blank_pil = Image.new("L", img_pil.size, 255)
    blank_draw = ImageDraw.Draw(blank_pil)

    results = run(gray_pil)
    for line in results:
        x, y, w, h = line[0]
        txt = line[1]
        t=''.join(txt)
        font = ImageFont.truetype("/home/yuvaraj/Downloads/input/msyh.ttf", max(int(h * 0.6), 14))
        blank_draw.text(xy=(x, y), text=txt, font=font)

    #blank_pil

    text=''
    results = run(gray_pil)
    for line in results:
        txt = line[1]+"  "
        font = ImageFont.truetype("/home/yuvaraj/Downloads/input/msyh.ttf", max(int(h * 0.6), 14))
        text+= ''. join(txt)

    aa=find_date(text)
    bb=find_date1(text)
    cc=find_date2(text)
    dd=find_date3(text)
    ee=find_date4(text)

    if is_date(aa)== True:
        print('date: ',aa)
        rk=aa
    elif (is_date(bb)==True):#&(bb[0:8]!=cc[0:8])
        print('date1: ',bb)
        rk=bb
    elif is_date(cc)==True:
        print('date2: ',cc)
        rk=cc
    elif is_date(dd)==True:
        print('date3: ',dd)
        rk=dd
    elif is_date(ee)==True:
        print('date4: ',ee)
        rk=ee
    else:
        rk='Opps..! Please choose cleared image'
    return str(rk)

print('Model loaded. Check http://127.0.0.1:5000/')



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        img = os.path.join(basepath, 'Receipts', secure_filename(f.filename))
        f.save(img)

        # Make prediction
        rk=image_text(img,find_date,find_date1,find_date2,find_date3,find_date4, is_date)
    return rk


if __name__ == '__main__':
    app.run(debug=True)

