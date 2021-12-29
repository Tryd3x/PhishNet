import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
#load XGBoost.pkl
model = pickle.load(open('XGBoostClassifier.pickle.dat', 'rb'))

@app.route('/')
def home():
    print("This is the homepage")
    return render_template("index.html",message = 'Welcome to PhishNet!')

@app.route('/predict',methods=['POST'])
def predict():
    #load data

    #parse data into features

    #predict using model

    #return output
    return

if __name__ == '__main__':
    app.run(debug=True)