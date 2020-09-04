import requests
from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load(open('crash_predictor.joblib', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    int_features = [int(x) for x in request.form.values()]
    print("int_features", int_features)
    final_features = [np.array(int_features)]
    print("final_features", final_features)
    prediction = model.predict(final_features)
    print("prediction", prediction)

    return render_template('index.html', prediction_text="hello")


if __name__ == "__main__":
    app.run(debug=True)
