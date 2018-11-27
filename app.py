from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
import re
from search import Search

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/search', methods=['POST'])
@cross_origin(supports_credentials=True)
def search():
    req_data = request.get_json()
    s = Search(req_data['query']).search()
    return jsonify(s)
