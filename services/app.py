from flask import Flask, request, render_template, send_from_directory
from os import listdir
from os.path import isfile, join, basename
from joblib import load
from nltk import tokenize
from werkzeug import secure_filename
from pandas import DataFrame, read_csv, concat, wide_to_long

## File upload location ##
UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = set(['csv'])

## Load Models ##
MODEL_PATH = './models/'
model_names = [m for m in listdir(MODEL_PATH) if isfile(join(MODEL_PATH, m)) and m.split('.')[1] == 'joblib']

models = {}
for code in model_names:
    models[basename(code)] = load(MODEL_PATH + code)

def row_to_segment(row):
    segments = tokenize.sent_tokenize(row[0])
    results = DataFrame({'text': row[0],
                         'segment': segments,
                         'state': row[1]})

    return results

def predict(narratives):
    successes = concat([row_to_segment(row) for index, row in 
                        narratives[["Task_Qtrly_Successes", "state"]]. \
                        dropna().iterrows()])
    successes["type"] = "Task_Qtrly_Successes"
    
    challenges = concat([row_to_segment(row) for index, row in 
                         narratives[["Task_Qtrly_Challenges", "state"]]. \
                         dropna().iterrows()])
    challenges["type"] = "Task_Qtrly_Challenges"

    results = concat([successes, challenges])
    results["id"] = range(0, len(results))

    for code, model in models.items():
        results["prediction;" + code.replace(".joblib", "")] = \
            model.predict(results["segment"])

    results = wide_to_long(results, 
                           stubnames="prediction", 
                           i=["text", "segment", "state", "type", "id"], 
                           j="code", 
                           sep=";", 
                           suffix="\w+")

    results = results[results.prediction > 0].reset_index()

    return results

def create_quotes(results):
    results_by_code = ''

    codes = results.code.unique()
    codes.sort()

    for code in codes:
        results_by_code = results_by_code \
                          + code + "\n\n" \
                          + "\n".join([seg+" ("+st+": "+ty+")" for seg,st,ty in zip(results.segment[results.code == code].tolist(),
                                                                                    results.state[results.code == code].tolist(),
                                                                                    results.type[results.code == code].tolist())]) \
                          + "\n\n"

    return results_by_code

## Application ##
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=["GET"])
def csv_form():
    return render_template('upload.html')

@app.route("/predict", methods=["GET","POST"])
def upload_and_predict_codes():
    file = request.files['file']
    if request.method == 'POST':
        narratives = read_csv(request.files.get('file'), 
                              encoding="ISO-8859-1")

        results = predict(narratives)

        results_by_code = create_quotes(results)

        path_txt_results =  join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename).replace('.csv','')+'_results.txt')

        with open(path_txt_results, 'w', encoding='utf-8') as outfile:
            outfile.write(results_by_code)

        return send_from_directory(app.config['UPLOAD_FOLDER'], 
                                   basename(path_txt_results), 
                                   as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
