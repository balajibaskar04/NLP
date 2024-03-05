import flask
from flask import Flask, render_template, request
from pdf2image import convert_from_path
import os
import cv2
import pytesseract
import pandas as pd
import re
import glob
from pandas import ExcelWriter
from PIL import Image
import datetime
import pathlib
import shutil
import webview


app = Flask(__name__, template_folder= './templates')
window = webview.create_window('NLP PROJECT!',  app)

# Create a route to the main page
@app.route('/')
def main_page():
    return render_template('login_dashboard_nlp.html')

#
# Create a route to handle the file upload
@app.route('/upload', methods=['POST'])
def handle_upload():
    uploaded_file_1 =  request.form['text_input']
    uploaded_file_2 =  request.form['text_input_1']
    folder_path = uploaded_file_1
    location_folder = folder_path + '/' + uploaded_file_2
    print("Folder dir", location_folder)
    os.chdir(location_folder)

    for iterate_folder in os.listdir(location_folder):
        iterate_each_folder = '/' + iterate_folder
        pdf_path = os.path.join(location_folder , iterate_each_folder)
        print("***************************start**********************************")

        # Mention the installed location of Tesseract-OCR in your system
        pytesseract.pytesseract.tesseract_cmd = uploaded_file_1 + r'\Tesseract-OCR\tesseract.exe'
        end_path = location_folder + '/' + iterate_folder
        os.chdir(end_path)
        #print("&&&&",os.getcwd())

        path = glob.glob("*.png")

        lst_corpus = []
        lst_folder_name = []

        for i, k in enumerate(path):

            img = cv2.imread(k)

            # Convert the image to gray scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Performing OTSU threshold
            ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

            # Applying dilation on the threshold image
            dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

            # Finding contours
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_NONE)

            # Creating a copy of image
            im2 = img.copy()
            for j, cnt in enumerate(contours):
                inner = ''
                x, y, w, h = cv2.boundingRect(cnt)
                # Drawing a rectangle on copied image
                rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Cropping the text block for giving input to OCR
                cropped = im2[y:y + h, x:x + w]
                ext_txt = pytesseract.image_to_string(cropped)
                lst_corpus.append(ext_txt)
                lst_folder_name.append(iterate_folder)
                file_path = "extract_text" + str(i) + ".txt"

                with open(file_path, 'w') as file:
                    file.write(str(ext_txt))


        print("Corpus", lst_corpus)
        print("folder_name", lst_folder_name)





        print("********************end**********************")


    return flask.render_template('result_page.html')

if __name__ == '__main__':
   #app.run(debug=True)
   webview.start()

