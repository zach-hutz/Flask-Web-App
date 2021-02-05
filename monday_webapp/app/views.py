from flask import render_template, request, redirect
from app import app
import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json


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

            def get_x_label():
                x_label = d_list[0]
                return x_label
            def get_y_label():
                y_label = d_list[1]
                return y_label
            def get_title():
                new_file = uploaded_file.filename.replace(".csv", "")
                return new_file
            def get_x_array():
                d_list = list(data.columns.values)
                x_label = d_list[0]
                data_x_array = np.array(data[x_label])
                return json.dumps(data_x_array)
            def get_y_array():
                d_list = list(data.columns.values)
                y_label = d_list[1]
                data_y_array = np.array(data[y_label])
                ydump = json.dumps(data_y_array)
                return ydump

            return render_template('index.html', datayarray=get_y_array(), dataxarray=get_x_array(), dataframe=data, x_label=get_x_label(), y_label=get_y_label(), chart_title=get_title(), tables=[data.to_html(classes='data')], titles=str(data.iloc[0]), header=False, index=False, index_names=False)
    return render_template('index.html', data=data)


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "C:\\Users\\Zachary\\Documents\\VSCode_Projects\\monday_webapp\\app\\static\\file\\uploads"
