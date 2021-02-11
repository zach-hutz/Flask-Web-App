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

            
            x_label = d_list[0]

            y_label = d_list[1]
            new_file = uploaded_file.filename.replace(".csv", "")

            data_x_array = list(data[x_label])
            data_y_array = list(data[y_label])
            data_y_array = [i.replace(" ", "") for i in data_y_array]
            data_y_array = [float(i) for i in data_y_array]   

            ydump = json.dumps(data_y_array)
            print(ydump)
            print(type(x_label))
            print(x_label)
            ident = json.dumps(x_label)
            print(ident)

            return render_template('index.html', identifier=x_label, datayarray=ydump, dataxarray=data_x_array, chart_name=new_file, tables=[data.to_html(classes='data')], titles=str(data.iloc[0]), header=False, index=False, index_names=False)
    return render_template('index.html', data=data)


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "monday_webapp\\app\\static\\file\\uploads"
