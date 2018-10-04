
from flask import Flask, jsonify, request, make_response
from sklearn.externals import joblib
from werkzeug.security import safe_str_cmp

import os

MODEL_NAME = "final_model_svc.pkl"
USER = "admin"
PASSWORD = "admin"

my_best_model = joblib.load(MODEL_NAME)

app = Flask(__name__)


@app.route("/submit", methods=['POST'])
def predict():

    try:
        username = request.authorization["username"]
        password = request.authorization["password"]

        if username or password:
            if not safe_str_cmp(username, USER) or not safe_str_cmp(password, PASSWORD):
                return make_response("Authentication Denied!", 401)

    except TypeError:
        return make_response("Please use authorization service to submit.", 401)

    try:
        request_data = request.get_json()
        message = request_data['text']
    except TypeError:
        return make_response("Invalid JSON format or request CONTENT-TYPE JSON", 400)
    else:
        pred_result = my_best_model.predict([message])
        answer = int(pred_result[0])

        return jsonify({ 'result': "Non-abusive" if answer == 0 else "Abusive" }), 200


if __name__ == "__main__":
     server = os.environ.get('SERVER_CYBER')
     if server is not None:
        app.run(host='0.0.0.0', port=5000)
     else:
        app.run(port=5000)
