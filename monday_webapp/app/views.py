from flask import render_template, request, redirect
from app import app
import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64


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
            data = pd.DataFrame(data[1:], columns=data[0])
            if len(data.columns) >=3:
                error_msg = 'Error please select a CSV with two columns'
                return error_msg

            d_list = list(data.columns.values)

            x_label = d_list[0]
            y_label = d_list[1]

            new_file = uploaded_file.filename.replace(".csv", "")

            fig = Figure()
            axis = fig.add_subplot(1, 1, 1)
            axis.set_title(new_file)
            axis.set_xlabel(x_label)
            axis.set_ylabel(y_label)
            axis.grid()
            axis.plot(data[x_label], data[y_label])

            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

            return render_template('index.html', image=pngImageB64String, tables=[data.to_html(classes='data')], titles=str(data.iloc[0]), header=False, index=False, index_names=False)
    return render_template('index.html', data=data)


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "C:\\Users\\Zachary\\Documents\\VSCode_Projects\\monday_webapp\\app\\static\\file\\uploads"
