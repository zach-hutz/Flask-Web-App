from flask import render_template, request, redirect
from app import app
import os
import csv
import pandas as pd
from matplotlib import pyplot as plt

@app.route('/', methods=["GET", "POST"])
def index():
    data = []
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath) as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row)
            data = pd.DataFrame(data)

            return render_template('index.html', tables=[data.to_html(classes='data')], titles=data.columns.values, header=False, index=False)
    return render_template('index.html', data=data)


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "C:\\Users\\Zachary\\Documents\\VSCode_Projects\\monday_webapp\\app\\static\\file\\uploads"

'''
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            uploaded_file.save(os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename))
            return redirect(request.url)

    return render_template('upload.html')
            a = [1,2,3,4]
            string_a = json.dumps(a)
'''

