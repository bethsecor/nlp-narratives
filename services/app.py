from flask import Flask, request, flash, redirect, url_for, render_template
from os import listdir
from os.path import isfile, join, basename
import joblib
from nltk import tokenize
import json
from werkzeug import secure_filename
import pandas
import math

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
    results = {}
    for seg in segments:
        model_results = {}
        for code, model in models.items():
            model_results[basename(code)] = str(model.predict([seg])[0])
        results[seg] = model_results
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
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
            
            results = {}
            for index, row in narratives.iterrows():
                results[row['state']] = {'successes': iterate_models(handle(row['Task_Qtrly_Successes'])), 
                                         'challenges': iterate_models(handle(row['Task_Qtrly_Challenges']))}
            
            return json.dumps(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
