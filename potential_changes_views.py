from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import render_template, request, redirect
from matplotlib.figure import Figure
import pandas as pd
from app import app
import base64
import csv
import io
import os

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

            def create_s_line_g():
                fig = Figure()
                axis = fig.add_subplot(1, 1, 1)
                axis.set_title(new_file)
                axis.set_xlabel(x_label)
                axis.set_ylabel(y_label)
                axis.grid()
                axis.plot(data[x_label], data[y_label])

                pngImageSLine = io.BytesIO()
                FigureCanvas(fig).print_png(pngImageSLine)
                pngImageSLineB64String = "data:image/png;base64,"
                pngImageSLineB64String += base64.b64encode(pngImageSLine.getvalue()).decode('utf8')
                return pngImageSLineB64String

           def create_s_bar_g():
               fig = Figure()
               axis = fig.add_subplot(1, 1, 1)
               axis.set_title(new_file)
               axis.set_xlabel(x_label)
               axis.set_ylabel(y_label)
               axis.grid()
               axis.barh(data[x_label], data[y_label])

               pngImageSBar = io.BytesIO()
               FigureCanvas(fig).print_png(pngImageSBar)
               pngImageSBarB64String = "data:image/png;base64,"
               pngImageSBarB64String += base64.b64encode(pngImageSBar.getvalue()).decode('utf8')
               return pngImageSBarB64String


           def create_stack_bar_g():
               fig = Figure()
               axis = fig.add_subplot(1, 1, 1)
               axis.set_title(new_file)
               axis.set_xlabel(x_label)
               axis.set_ylabel(y_label)
               axis.grid()
               axis.bar(data[x_label], data[y_label])

               pngImageSTBar = io.BytesIO()
               FigureCanvas(fig).print_png(pngImageSTBar)
               pngImageSTBarB64String = "data:image/png;base64,"
               pngImageSTBarB64String += base64.b64encode(pngImageSTBar.getvalue()).decode('utf8')
               return pngImageSTBarB64String


           create_s_line_g()
           create_s_bar_g()
           create_stack_bar_g()
# Change src "image" to "imagesline" in index

            return render_template('index.html', imagestbar=pngImageSTBarB64String, imagesline=pngImageSLineB64String, imagesbar=pngImageSBarB64String ,tables=[data.to_html(classes='data')], titles=str(data.iloc[0]), header=False, index=False, index_names=False)
    return render_template('index.html', data=data)


@app.route('/help')
def help():
    return render_template('help.html')

app.config['FILE_UPLOADS'] = "C:\\Users\\Zachary\\Documents\\VSCode_Projects\\monday_webapp\\app\\static\\file\\uploads"
