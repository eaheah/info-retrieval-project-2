from flask import Flask
from flask import request
from flask import jsonify

from search import Search

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def search():
    req_data = request.get_json()
    s = Search(req_data['query']).search()
    return jsonify(s)