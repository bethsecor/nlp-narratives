from flask import Flask, request
from os import listdir
from os.path import isfile, join, basename
import joblib

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
    narrative = request.json["narrative"]
    
    return "test: " + narrative

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
