from flask import Flask, request
from os import listdir
from os.path import isfile, join, basename
import joblib
from nltk import tokenize
import json

## Load Models ##
path = './models/'
model_names = [m for m in listdir(path) if isfile(join(path, m)) and m.split('.')[1] == 'joblib']

models = {}
for code in model_names:
    models[basename(code)] = joblib.load(path + code)

## Application ##
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_codes():
    segments = tokenize.sent_tokenize(request.json['narrative'])
    print(segments) 
    results = {}
    for seg in segments:
        model_results = {}
        for code, model in models.items():
            print(code)
            model_results[basename(code)] = str(model.predict([seg])[0])
        results[seg] = model_results
    print(results)
    return json.dumps(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
