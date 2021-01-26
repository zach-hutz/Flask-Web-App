from flask import render_template, request, redirect
from app import app
import os

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "C:\\Users\\Zachary\\Documents\\VSCode_Projects\\monday_webapp\\app\\static\\file\\uploads"

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            uploaded_file.save(os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename))
            return redirect(request.url)

    return render_template('upload.html')


