from flask import (Flask, render_template, request)
import pandas as pd
import numpy as np
import joblib
import pickle

app = Flask(__name__)
model = joblib.load(open("crash_predictor2.pkl", "rb"))
# prediction function


@app.route('/')
def home():
    return render_template('index_test.html')


@app.route('/predict', methods=['POST'])
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 8)
    result = model.predict(to_predict)
    return result[0]


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        if int(result) == 1:
            prediction = 'Too bad, YOU DEAD'
        else:
            prediction = 'You Survived!'
        return render_template("index_test.html", prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
