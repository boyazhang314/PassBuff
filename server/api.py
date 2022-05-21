from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

def tokenization(word):
    tokens = []
    for ch in word:
        tokens.append(ch)
    return tokens

from power import power

# configuration
DEBUG = True

# server
PASSWORD = [{"password": ""}]

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
@cross_origin(origins = "http://localhost:5000")

# sanity check route
@app.route('/power', methods=['GET', 'POST'])
def buffer():
    response = {'status': 'success'}
    if request.method == 'POST':
        post = request.get_json()
        PASSWORD[0]["password"] = post.get("password")
        response['message'] = "Password Updated!"
    else:
        response['power'] = power(PASSWORD[0]["password"])
    # json
    response = jsonify(response)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':
    app.run()