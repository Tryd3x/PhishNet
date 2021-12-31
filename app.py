import numpy as np
from flask import Flask, json, request, jsonify, render_template
from flask_cors import CORS
import pickle
from URLFeatureExtraction import featureExtraction,feature_names
import pandas as pd

app = Flask(__name__)
CORS(app)
#load XGBoost.pkl
model = pickle.load(open('XGBoostClassifier.pickle.dat', 'rb'))

@app.route('/')
def home():
    print("This is the homepage")
    return render_template("index.html",message = 'Welcome to PhishNet!')

@app.route('/predict',methods=['POST'])
def predict():
    try:
        #load data
        data = request.get_json(force=True)
        url = data['url']

        #parse data into features
        features_extracted = featureExtraction(url)
        print(len(features_extracted))
        print(features_extracted)
        df = pd.DataFrame(features_extracted).transpose()
        df.columns = feature_names
        # print(df)

        prediction = model.predict(df)
        prediction = prediction.tolist()
        return jsonify(prediction)
        # print(type(prediction.tolist()))
    except Exception as e:
        return jsonify(e)

    #return output
    
    # return render_template("index.html",message = 'Welcome to PhishNet!')

if __name__ == '__main__':
    app.run(debug=True)