from flask import render_template, request, redirect
from app import app
import os
import csv
import pandas as pd


@app.route('/', methods=["GET", "POST"])
def index():
    data = []
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename'] # This line uses the same variable and worked fine
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath) as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row)
            data = pd.DataFrame(data)
            return render_template('index.html', data=data.to_html(header=False, index=False))
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
'''

