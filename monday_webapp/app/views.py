from flask import render_template, request, redirect
from app import app
import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
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
            file_name = uploaded_file.filename.replace(".csv", "")

            data_x_array = list(data[x_label])
            data_y_array = list(data[y_label])
            data_y_array = [i.replace(" ", "") for i in data_y_array]
            data_y_array = [float(i) for i in data_y_array]

            graph_label = []
            graph_label.append(x_label)
            graph_label.append(y_label)
            graph_label = [i.replace('"', '') for i in graph_label]
            graph_label = [i.replace('"', '') for i in graph_label]
            print("GRAPH_LABEL - " + str(graph_label))   

            ydump = json.dumps(data_y_array)
            print("YDUMP - " + str(ydump))
            print("X_LABEL - " + x_label)
            print("Y LABEL - " + y_label)
            
            
            print(data_x_array)
            xdump = json.dumps(data_x_array)
            print(xdump)
            print(xdump)

            return render_template('index.html', graphlabel=graph_label, y_label=y_label, datayarray=ydump, dataxarray=xdump, chart_name=file_name, tables=[data.to_html(classes='data')], titles=str(data.iloc[0]), header=False, index=False, index_names=False)
    return render_template('index.html', data=data)


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "monday_webapp\\app\\static\\file\\uploads"
