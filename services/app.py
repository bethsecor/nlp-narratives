from flask import Flask, request, flash, redirect, url_for, render_template
from os import listdir
from os.path import isfile, join, basename
import joblib
from nltk import tokenize
import json
from werkzeug import secure_filename
import pandas
import math
import numpy

## File upload location ##
UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## Load Models ##
MODEL_PATH = './models/'
model_names = [m for m in listdir(MODEL_PATH) if isfile(join(MODEL_PATH, m)) and m.split('.')[1] == 'joblib']

models = {}
for code in model_names:
    models[basename(code)] = joblib.load(MODEL_PATH + code)

## Iterate over models ##
def iterate_models(text):
    segments = tokenize.sent_tokenize(text)
    results = pandas.DataFrame({'code':[],
                                'segment':[],
                                'prediction':[]})
    for seg in segments:
        for code, model in models.items():
            results = results.append(pandas.DataFrame({'code':[code.replace('.joblib','')], 
                                                       'segment':[seg], 
                                                       'prediction':[model.predict([seg])[0]]}), sort=False)
    results = results[results.prediction > 0]
    return results

## Check CSV for empty cells
def handle(cell):
    if not isinstance(cell, str) and math.isnan(cell):
        return ''
    else:
        return cell

## Application ##
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=["GET"])
def csv_form():
    return render_template('upload.html')

@app.route("/predict", methods=["GET","POST"])
def upload_and_predict_codes():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file.')
            return redirect(request.url_for('csv_form'))
        file = request.files['file']
        if file.filename == '':
            #flash('No file selected.')
            return redirect(url_for('csv_form'))
        elif not allowed_file(file.filename):
            #flash('File not a CSV')
            return redirect(url_for('csv_form'))
        else:
            path_file = join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(path_file)
            print("File saved here: " + path_file)
            narratives = pandas.read_csv(path_file, encoding = "ISO-8859-1")    
            
            results =  pandas.DataFrame({'code':[],
                                         'segment':[],
                                         'prediction':[],
                                         'state':[],
                                         'type':[]})
            for index, row in narratives.iterrows():
                successes =  iterate_models(handle(row['Task_Qtrly_Successes']))
                successes['type'] = 'Task_Qtrly_Successes'
                successes['state'] = row.state
                challenges = iterate_models(handle(row['Task_Qtrly_Challenges']))
                challenges['type'] = 'Task_Qtrly_Challenges'
                challenges['state'] = row.state
                results = results.append([successes, challenges],sort=False)

            results_by_code = ''
            for code in numpy.unique(results.code):
                results_by_code = results_by_code \
                                  + code + "\n\n" \
                                  + "\n".join([seg+" ("+st+": "+ty+")" for seg,st,ty in zip(results.segment[results.code == code].tolist(),
                                                                                            results.state[results.code == code].tolist(),
                                                                                            results.type[results.code == code].tolist())]) \
                                  + "\n\n"

            path_txt_results =  join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename).replace('.csv','')+'_results.txt')
            print(path_txt_results)
            with open(path_txt_results, 'w') as outfile:
                outfile.write(results_by_code)

            return results_by_code

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
